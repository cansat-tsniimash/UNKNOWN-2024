/*
 * app_main.c
 *	С НОВЫМ ГОДОМ ЭЩКЕРЕЕ
 *  Created on: Sep 20, 2023
 *      Author: Install
 */
#include "main.h"
#include "Shift_Register/shift_reg.h"
#include <LSM6DS3/DLSM.h>
#include <LIS3MDL/DLIS3.h>
#include <string.h>
#include <stdio.h>
#include "csv_file.h"
#include "structs.h"
#include <fatfs.h>
#include <ATGM336H/nmea_gps.h>
#include <nRF24L01_PL/nrf24_upper_api.h>
#include <nRF24L01_PL/nrf24_lower_api_stm32.h>
#include <nRF24L01_PL/nrf24_defs.h>
#include <BME280_I2C/its_bme280.h>
#include <BME280_I2C/bme280_defs.h>
#include <BME280_I2C/bme280.h>
#include "ina219/inc/ina219_helper.h"
#include <Photorezistor/photorezistor.h>
#include "madgwick.h"
#include "DWT_Delay/dwt_delay.h"

extern SPI_HandleTypeDef hspi5;
extern SPI_HandleTypeDef hspi1;
extern UART_HandleTypeDef huart1;
extern UART_HandleTypeDef huart2;
extern SPI_HandleTypeDef hspi4;
extern I2C_HandleTypeDef hi2c1;
extern ADC_HandleTypeDef hadc1;

void rotate_sm(double angle, bool side){
	double steps = angle*2/0.0325791855;
	if(steps>22100){
		steps = 22100;
	}

	HAL_GPIO_WritePin(GPIOA, GPIO_PIN_10, side);
	for(int i = 0; i<steps; i++){
		HAL_GPIO_WritePin(GPIOA, GPIO_PIN_9, true);
		dwt_delay_us(70);
		HAL_GPIO_WritePin(GPIOA, GPIO_PIN_9, false);
		dwt_delay_us(70);
	}

}

/*int _write(int file, char *ptr, int len)
{
	HAL_UART_Transmit(&huart1, (uint8_t *)ptr, len, 100);
	return 0;
}*/

typedef enum
{
	STATE_GEN_PACK_2 = 1,
	STATE_WAIT = 2,
	STATE_GEN_PACK_1_Q = 3,
	STATE_GEN_PACK_3 = 4,
} state_nrf_t;

typedef enum
{
	STATE_READY = 0,
	STATE_IN_ROCKET = 1,
	STATE_AFTER_ROCKET = 2,
	STATE_STABILZATORS = 3,
	STATE_DESCENT = 4,
	STATE_ON_EARTH = 5
} state_t;

typedef struct INA219_DATA{
	uint16_t power;
	uint16_t current;
	uint16_t voltage;
	uint16_t shunt_voltage;
}INA219_DATA;

void nrf_dump_regs(nrf24_lower_api_config_t * lower);

uint16_t Crc16(uint8_t *buf, uint16_t len) {
	uint16_t crc = 0xFFFF;
	while (len--) {
		crc ^= *buf++ << 8;
		for (uint8_t i = 0; i < 8; i++)
			crc = crc & 0x8000 ? (crc << 1) ^ 0x1021 : crc << 1;
	}
	return crc;
}

int app_main(){
	//файлы
	FATFS fileSystem; // переменная типа FATFS
	FIL File1; // хендлер файла
	FIL File2;
	FIL File3;
	FIL Fileq;
	FIL Fileb;
	FRESULT res1 = 255;
	FRESULT res2 = 255;
	FRESULT res3 = 255;
	FRESULT resb = 255;
	FRESULT resq = 255;
	FRESULT res_bin = 255;
	FRESULT megares = 255;
	const char path1[] = "packet1.csv";
 	const char path2[] = "packet2.csv";
 	const char path3[] = "packet3.csv";
 	const char pathq[] = "quaternion.csv";
 	const char pathb[] = "packet.bin";

	memset(&fileSystem, 0x00, sizeof(fileSystem));
	FRESULT is_mount = 0;
	extern Disk_drvTypeDef disk;
	disk.is_initialized[0] = 0;
	is_mount = f_mount(&fileSystem, "", 1);
	if(is_mount == FR_OK) { // монтируете файловую систему по пути SDPath, проверяете, что она смонтировалась, только при этом условии начинаете с ней работать
		res1 = f_open(&File1, (char*)path1, FA_WRITE | FA_CREATE_ALWAYS); // открытие файла, обязательно для работы с ним
		f_puts("num; time; accl1; accl2; accl3; gyro1; gyro2; gyro3; mag1; mag2; mag3\n", &File1);
		res1 = f_sync(&File1);
	}
	if(is_mount == FR_OK) { // монтируете файловую систему по пути SDPath, проверяете, что она смонтировалась, только при этом условии начинаете с ней работать
		res2 = f_open(&File2, (char*)path2, FA_WRITE | FA_CREATE_ALWAYS); // открытие файла, обязательно для работы с ним
		f_puts("num; time; bmp_temp; bmp_press; bmp_humidity; bmp_height; photorez\n", &File2);
		res2 = f_sync(&File2);
	}
	if(is_mount == FR_OK) { // монтируете файловую систему по пути SDPath, проверяете, что она смонтировалась, только при этом условии начинаете с ней работать
		res3 = f_open(&File3, (char*)path3, FA_WRITE | FA_CREATE_ALWAYS); // открытие файла, обязательно для работы с ним
		f_puts("num; time; fix; lat; lon; alt; times; timems\n", &File3);
		res3 = f_sync(&File3);
	}
	if(is_mount == FR_OK) { // монтируете файловую систему по пути SDPath, проверяете, что она смонтировалась, только при этом условии начинаете с ней работать
		resq = f_open(&Fileq, (char*)pathq, FA_WRITE | FA_CREATE_ALWAYS); // открытие файла, обязательно для работы с ним
		f_puts("", &Fileq);
		resq = f_sync(&Fileq);
	}
	if(is_mount == FR_OK){
		resb = f_open(&Fileb, pathb, FA_WRITE | FA_OPEN_APPEND);
	}

	//переменные
	uint8_t counter = 0;
	state_nrf_t state_nrf;
	state_nrf = STATE_GEN_PACK_2;
	uint32_t start_time_nrf = HAL_GetTick();
	nrf24_fifo_status_t rx_status = NRF24_FIFO_EMPTY;
	nrf24_fifo_status_t tx_status = NRF24_FIFO_EMPTY;
	float temperature_celsius_gyro = 0.0;
	float acc_g[3] = {0};
	float gyro_dps[3] = {0};
	float temperature_celsius_mag = 0.0;
	float mag[3] = {0};
	float gyro_m[3] = {0};
	float acc_m[3] = {0};
	float lat;
	float lon;
	float alt;
	float lats;
	float lons;
	float alts;
	uint32_t timefv1 = 200000000;
	uint32_t timefv2 = 200000000;
	uint32_t timefv3 = 200000000;
	uint32_t timefv4 = 200000000;
	uint32_t start_time_par = 0;
	uint32_t start_time_stab = 0;
	uint32_t start_time_luxes = 0;
	float time_now = 0;
	float time_before = 0;

	int fix_;
	float limit_lux;
	int comp = 0;
	int64_t cookie;
	uint16_t str_wr;
	UINT Bytes;
	char str_buf[300];
	float seb_quaternion [4] = {0};
	double bmp_temp;
	double bmp_press;
	double bmp_humidity;
	//сдвиговый регистр

	shift_reg_t shift_reg_r;
	shift_reg_r.bus = &hspi1;
	shift_reg_r.latch_port = GPIOB;
	shift_reg_r.latch_pin = GPIO_PIN_14;
	shift_reg_r.oe_port = GPIOA;
	shift_reg_r.oe_pin = GPIO_PIN_8;
	shift_reg_r.value = 0;
	shift_reg_init(&shift_reg_r);
	shift_reg_write_8(&shift_reg_r, 0x00);
	state_t state_now;
	state_now = STATE_READY;
	shift_reg_write_bit_8(&shift_reg_r, 7, 0);
	//работа бме
	/*struct bme_spi_intf_sr bme_struct;
	bme_struct.sr_pin = 2;
	bme_struct.sr = &shift_reg_r;
	bme_struct.spi = &hspi5;
	struct bme280_dev bme;
	bme_init_default_sr(&bme, &bme_struct);
	struct bme280_data bme_data;
	bme_data = bme_read_data(&bme);*/

	bme_important_shit_t bme_shit;
	its_bme280_init(UNKNOWN_BME);
	its_bme280_read(UNKNOWN_BME, &bme_shit);
/*	//ina
	struct ina219_t ina219;
	ina219_primary_data_t primary_data;
	ina219_secondary_data_t secondary_data;
	ina219_init_default(&ina219,&hi2c1,INA219_I2CADDR_A1_GND_A0_VSP, HAL_MAX_DELAY);
	int ina_res;
	float current;
	float bus_voltage;*/
	//стх и структура лcмa
	stmdev_ctx_t ctx_lsm;
	struct lsm_spi_intf_sr lsm_sr;
	lsm_sr.sr_pin = 6;
	lsm_sr.spi = &hspi1;
	lsm_sr.sr = &shift_reg_r;
	lsmset_sr(&ctx_lsm, &lsm_sr);
	//photorez
	photorezistor_t photrez;
	photrez.resist = 2200;
	photrez.hadc = &hadc1;

	//настройка радио
	nrf24_spi_pins_t nrf_pins;
	nrf_pins.ce_port = GPIOC;
	nrf_pins.cs_port = GPIOC;
	nrf_pins.ce_pin = GPIO_PIN_13;
	nrf_pins.cs_pin = GPIO_PIN_14;
	nrf24_lower_api_config_t nrf24;
	nrf24_spi_init(&nrf24, &hspi4, &nrf_pins);

	printf("before setup\n");
	nrf_dump_regs(&nrf24);

	nrf24_mode_power_down(&nrf24);
	nrf24_rf_config_t nrf_config;
	nrf_config.data_rate = NRF24_DATARATE_250_KBIT;
	nrf_config.tx_power = NRF24_TXPOWER_MINUS_0_DBM;
	nrf_config.rf_channel = 10;		//101;
	nrf24_setup_rf(&nrf24, &nrf_config);
	nrf24_protocol_config_t nrf_protocol_config;
	nrf_protocol_config.crc_size = NRF24_CRCSIZE_1BYTE;
	nrf_protocol_config.address_width = NRF24_ADDRES_WIDTH_5_BYTES;
	nrf_protocol_config.en_dyn_payload_size = true;
	nrf_protocol_config.en_ack_payload = false;
	nrf_protocol_config.en_dyn_ack = false;
	nrf_protocol_config.auto_retransmit_count = 0;
	nrf_protocol_config.auto_retransmit_delay = 0;
	nrf24_setup_protocol(&nrf24, &nrf_protocol_config);
	nrf24_pipe_set_tx_addr(&nrf24, 0xacacacacac);

	nrf24_pipe_config_t pipe_config;
	for (int i = 1; i < 6; i++)
	{
		pipe_config.address = 0xacacacacac;
		pipe_config.address = (pipe_config.address & ~((uint64_t)0xff << 32)) | ((uint64_t)(i + 7) << 32);
		pipe_config.enable_auto_ack = false;
		pipe_config.payload_size = -1;
		nrf24_pipe_rx_start(&nrf24, i, &pipe_config);
	}

	pipe_config.address = 0xafafafaf01;
	pipe_config.enable_auto_ack = false;
	pipe_config.payload_size = -1;
	nrf24_pipe_rx_start(&nrf24, 0, &pipe_config);

	nrf24_mode_standby(&nrf24);
	printf("\n\n");
	printf("after setup\n");
	nrf_dump_regs(&nrf24);
	printf("\n\n");
	nrf24_mode_tx(&nrf24);

	uint16_t num1 = 0;
	uint16_t num2 = 0;
	uint16_t num3 = 0;
	uint16_t num4 = 0;
	int a = 6378000;
	int b = 6357000;
	uint32_t gps_time_s;
	uint32_t gps_time_us;
	//gps
	gps_init();
	gps_work();
	gps_get_coords(&cookie, &lats, &lons, &alts, &fix_);
	gps_get_time(&cookie, &gps_time_s, &gps_time_us);
	double b2da2 = (b*b)/(a*a);
	double nb = (a*a)/sqrt((a*a)* (cos(lats)*cos(lats) + (b*b) * ((sin(lats) * sin(lats)))));
	double x_gpss = (nb + alts)* cos(lats) * cos(lons);
	double y_gpss = (nb + alts)* cos(lats) * sin(lons);
	double z_gpss = (b2da2*nb + alts) * sin(lats);

	double matrix1[3][3] =
	{{-sin(lons), cos(lons), 0},
	{(-sin(lats)*cos(lons)), (-sin(lats)*sin(lons)), cos(lats)},
	{cos(lats)*cos(lons), cos(lats)*sin(lons), sin(lats)}};

	/*char str1[60]={0};
	HAL_UART_Receive_IT(&huart1,(uint8_t*)str1,1);
	uint8_t bluetooth_recive = 1;
	HAL_UART_Receive_IT(&huart2, &bluetooth_recive, 1);*/
	__HAL_UART_ENABLE_IT(&huart2, UART_IT_RXNE);
	__HAL_UART_ENABLE_IT(&huart2, UART_IT_ERR);

	//стх и структура лиса
	stmdev_ctx_t ctx_lis;
	struct lis_spi_intf_sr lis_sr;
	lis_sr.sr_pin = 2;
	lis_sr.spi = &hspi1;
	lis_sr.sr = &shift_reg_r;
	lisset_sr(&ctx_lis, &lis_sr);
	int16_t magg[3];
	int16_t gyro[3];
	pack1_t pack1 = {0};
	pack2_t pack2 = {0};
	pack3_t pack3 = {0};
	packq_t packq = {0};
	pack1.flag = 0xAA;
	pack2.flag = 0xBB;
	pack3.flag = 0xCC;
	packq.flag = 0xFF;
	//давление на земле
	its_bme280_read(UNKNOWN_BME, &bme_shit);
	double ground_pressure = bme_shit.pressure;
	bmp_temp = bme_shit.temperature * 100;
	bmp_press = bme_shit.pressure;
	bmp_humidity = bme_shit.humidity;
	float height = 44330 * (1 - pow(bmp_press / ground_pressure, 1.0 / 5.255));
	float ground_height = 44330 * (1 - pow(bmp_press / ground_pressure, 1.0 / 5.255));
	ground_height += 30;
	int cntcnt = 0;
	int anglee = 120;
	float sca = 0;
	float rot = 0;
	while(1){
		//bme280
		float start = HAL_GetTick();
		its_bme280_read(UNKNOWN_BME, &bme_shit);
		bmp_temp = bme_shit.temperature * 100;
		bmp_press = bme_shit.pressure;
		bmp_humidity = bme_shit.humidity;
		float angle = 123.321;
		const uint8_t * angle_bytes = (const uint8_t*)&angle;
		uint8_t frame[] = {0xAA, 0xBB, 0xCC, 0x01, angle_bytes[0], angle_bytes[1], angle_bytes[2], angle_bytes[3]};
		//HAL_UART_Transmit(&huart1, frame, sizeof(frame), HAL_MAX_DELAY);
		height = 44330 * (1 - pow(bmp_press / ground_pressure, 1.0 / 5.255));
		float lux = 22.91;
		lux = photorezistor_get_lux(photrez);


		double alpha = 15.3; double beta = 13.5;

		//gps
		gps_work();
		gps_get_coords(&cookie, &lat, &lon, &alt, &fix_);
		gps_get_time(&cookie, &gps_time_s, &gps_time_us);
		lat = 55.91065;
		lon = 37.80538;
		alt = 200.0000;
		pack3.fix = fix_;
		pack3.lat = lat;
		pack3.lon = lon;
		pack3.alt = alt;
		double b2da2 = (b*b)/(a*a);
		double nb = (a*a)/sqrt((a*a)* (cos(lat)*cos(lat) + (b*b) * ((sin(lat) * sin(lat)))));
		double x_gps = (nb + alt)* cos(lat) * cos(lon);
		double y_gps = (nb + alt)* cos(lat) * sin(lon);
		double z_gps = (b2da2*nb + alt) * sin(lat);

		double matrix2[3][1] =
		{{x_gps - x_gpss},
		 {y_gps - y_gpss},
		 {z_gps - z_gpss}};

		double matrix3[3][1] =
		{{0},
		{0},
		{0}};

		for(int i = 0; i < 3; i++)
		    for(int j = 0; j < 1; j++)
		    {
		    	matrix3[i][j] = 0;
		        for(int k = 0; k < 3; k++)
		        	matrix3[i][j] += matrix1[i][k] * matrix2[k][j];
		    }
		for(int i = 0; i < 3; i++){
			for(int j = 0; j<1; j++){
				matrix3[i][j] *= -1;
			}
		}
		//lsm и lis

		lsmread(&ctx_lsm, &temperature_celsius_gyro, &acc_g, &gyro_dps);
		lisread(&ctx_lis, &temperature_celsius_mag, &mag);
		lsm6ds3_angular_rate_raw_get(&ctx_lsm, gyro);
		lis3mdl_magnetic_raw_get(&ctx_lis, magg);
		gyro[0] += 460;
		gyro[1] += 4830;
		gyro[2] += 3850;
		gyro_dps[0] += 0.46;
		gyro_dps[1] += 4.83;
		gyro_dps[2] += 3.85;
		gyro_m[0] = gyro_dps[0] * 3.14 / 180;
		gyro_m[1] = gyro_dps[1] * 3.14 / 180;
		gyro_m[2] = gyro_dps[2] * 3.14 / 180;
		acc_m[0] = acc_g[0] * 9.81;
		acc_m[1] = acc_g[1] * 9.81;
		acc_m[2] = acc_g[2] * 9.81;
		time_now = HAL_GetTick() / 1000.0;
		MadgwickAHRSupdate(seb_quaternion, gyro_m[0], gyro_m[1], gyro_m[2], acc_m[0], acc_m[1], acc_m[2], mag[0], mag[1], mag[2], time_now-time_before, 0.3);
		/*MadgwickAHRSupdateIMU(seb_quaternion, gyro_m[0], gyro_m[1], gyro_m[2], acc_m[0], acc_m[1], acc_m[2], time_before-time_now, 0.3);*/
		packq.times = time_now;
		time_before = time_now;
		//printf("%f	%f	%f	%f	%f\n", time_now, seb_quaternion[0], seb_quaternion[1], seb_quaternion[2], seb_quaternion[3]);
		/*printf("%f	%f	%f\n", gyro_dps[0], gyro_dps[1], gyro_dps[2]);*/

		packq.q1 = seb_quaternion[0];
		packq.q2 = seb_quaternion[1];
		packq.q3 = seb_quaternion[2];
		packq.q4 = seb_quaternion[3];
		double quat_vec[4] = {0, matrix3[0][0], matrix3[0][1], matrix3[0][2]};
		double quat_mid[4] = {seb_quaternion[0] * quat_vec[0] - seb_quaternion[1] * quat_vec[1] - seb_quaternion[2] * quat_vec[2] - seb_quaternion[3] * quat_vec[3],
				seb_quaternion[0] * quat_vec[1] + seb_quaternion[1] * quat_vec[0] + seb_quaternion[2] * quat_vec[3] - seb_quaternion[3] * quat_vec[2],
				seb_quaternion[0] * quat_vec[2] - seb_quaternion[1] * quat_vec[3] + seb_quaternion[2] * quat_vec[0] + seb_quaternion[3] * quat_vec[1],
				seb_quaternion[0] * quat_vec[3] + seb_quaternion[1] * quat_vec[2] - seb_quaternion[2] * quat_vec[1] + seb_quaternion[3] * quat_vec[0]};
		double quat_rev[4] = {seb_quaternion[0], seb_quaternion[1], seb_quaternion[2], seb_quaternion[3]};

		double quat_end[4] = {quat_mid[0] * quat_rev[0] - quat_mid[1] * quat_rev[1] - quat_mid[2] * quat_rev[2] - quat_mid[3] * quat_rev[3],
				quat_mid[0] * quat_rev[1] + quat_mid[1] * quat_rev[0] + quat_mid[2] * quat_rev[3] - quat_mid[3] * quat_rev[2],
				quat_mid[0] * quat_rev[2] - quat_mid[1] * quat_rev[3] + quat_mid[2] * quat_rev[0] + quat_mid[3] * quat_rev[1],
				quat_mid[0] * quat_rev[3] + quat_mid[1] * quat_rev[2] - quat_mid[2] * quat_rev[1] + quat_mid[3] * quat_rev[0]};

		double delta = atan(quat_end[1]/quat_end[2]) * 63.66;
		double ksi = atan((sqrt((quat_end[1]*quat_end[1]) + (quat_end[2]*quat_end[2])))/quat_end[3]) * 63.66;
		if(resq == FR_OK){
			str_wr = sd_parse_to_bytes_quaterneon(str_buf, &packq);
			resq = f_write(&Fileq, str_buf, str_wr, &Bytes); // отправка на запись в файл
			resq = f_sync(&Fileq);
		}

		/*printf("%d\n", HAL_GetTick());*/
		/*//ina
		ina_res = ina219_read_primary(&ina219,&primary_data);
		if (ina_res == 2)
		{
			I2C_ClearBusyFlagErratum(&hi2c1, 20);
		}
		ina_res = ina219_read_secondary(&ina219,&secondary_data);
		if (ina_res == 2)
		{
			I2C_ClearBusyFlagErratum(&hi2c1, 20);
		}
		//НЕ ЗАБЫТЬ ПОМЕНЯТЬ КОоФИЦЕТ!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
		current = ina219_current_convert(&ina219, secondary_data.current) * 0.67034;
		bus_voltage = ina219_bus_voltage_convert(&ina219, primary_data.busv) * 1.0399;*/
		//Photorez

 		//rotate_sm(5, 1);
 		uint8_t message[] = {'a', 'n', 'g', 'l', 'e', 0x00, 0x00, 0x00, 0x00};
 		uint8_t array[8] = {'s', 't', 'a', 'r', 't', 0xFF};
 		uint8_t array1[6] = {'s', 't', 'o', 'p', 0, 0xFF};
 //		HAL_UART_Transmit(&huart1, array, sizeof(array), 100);
 		/*float value = ;
 		memcpy(message + 7, &value, sizeof(value));*/
 		//rotate_sm(10, 1);
 		/*if(cntcnt <= 1)
		{
			HAL_UART_Transmit(&huart1, array, sizeof(array), 100);
		}
		if(cntcnt == 2)
		{
			char buffer[40] = {};
			const int len = snprintf(buffer, sizeof(buffer), "angle %d\n", anglee);
			HAL_UART_Transmit(&huart1, (uint8_t *)buffer, len, 100);
		}
		if(cntcnt > 50)
		{
			HAL_UART_Transmit(&huart1, array1, sizeof(array1), 100);
		}*/
		switch (state_now)
				{
				case STATE_READY:
					//HAL_Delay(100);
					HAL_UART_Transmit(&huart1, array, sizeof(array), 100);
					gps_get_coords(&cookie, &lats, &lons, &alts, &fix_);
					lats = 55.91119444;
					lons = 37.80572222;
					alts = 100.0000000;
					b2da2 = (b*b)/(a*a);
					nb = (a*a)/sqrt((a*a)* (cos(lats)*cos(lats) + (b*b) * ((sin(lats) * sin(lats)))));
					x_gpss = (nb + alts)* cos(lats) * cos(lons);
					y_gpss = (nb + alts)* cos(lats) * sin(lons);
					z_gpss = (b2da2*nb + alts) * sin(lats);
					if(HAL_GPIO_ReadPin(GPIOB, GPIO_PIN_12)){
						state_now = STATE_IN_ROCKET;
						start_time_luxes = HAL_GetTick();
						limit_lux = lux * 0.8;
					}
					break;
				case STATE_IN_ROCKET:
					rot = ksi-sca;
					sca += rot;
					if(rot >= 2){
						if(rot >= 0)
							rotate_sm(rot, 0);
						else
							rotate_sm(rot*-1, 1);
					}
					char buffer[40] = {};
					const int len = snprintf(buffer, sizeof(buffer), "angle %f\n", delta);
					HAL_UART_Transmit(&huart1, (uint8_t *)buffer, len, 100);
					/*if (HAL_GetTick()-start_time_luxes >= 300010000){
						if(lux >=  limit_lux){
							state_now = STATE_AFTER_ROCKET;
							start_time_par = HAL_GetTick();
						}
					}*/
					break;
				case STATE_AFTER_ROCKET:
					if (HAL_GetTick()-start_time_par >= 1488)
					{
						state_now = STATE_STABILZATORS;
						start_time_stab = HAL_GetTick();
					}
					break;
				case STATE_STABILZATORS:
					shift_reg_write_bit_8(&shift_reg_r, 1, 1);
					HAL_UART_Transmit(&huart1, array, sizeof(array), 100);
					if (HAL_GetTick()-start_time_stab >= 500)
					{
						shift_reg_write_bit_8(&shift_reg_r, 1, 0);
						state_now = STATE_DESCENT;
					}
					break;
				case STATE_DESCENT:
					//наведение
					rot = ksi-sca;
					sca += rot;
					if(rot >= 0)
						rotate_sm(rot, 0);
					else
						rotate_sm(rot*-1, 1);
					/*char buffer[40] = {};
					const int len = snprintf(buffer, sizeof(buffer), "angle %f\n", delta);*/
					//HAL_UART_Transmit(&huart1, (uint8_t *)buffer, len, 100);
					if(height <= ground_height){
						//state_now = STATE_ON_EARTH;
					}
					break;
				case STATE_ON_EARTH:
					//ыкл камеры и вкл пищалки
					HAL_GPIO_WritePin(GPIOB, GPIO_PIN_0, 1);

					HAL_UART_Transmit(&huart1, array1, sizeof(array1), 100);
					state_now = STATE_ON_EARTH;
					break;
				}
/*		typedef enum
		{
			STATE_READY = 0,
			STATE_IN_ROCKET = 1,
			STATE_AFTER_ROCKET = 2,
			STATE_STABILZATORS = 3,
			STATE_DESCENT = 4,
			STATE_ON_EARTH = 5
		} state_t;*/
		pack1.time_ms = HAL_GetTick();
		packq.time_ms = HAL_GetTick();
		pack2.bmp_temp = bmp_temp;
		pack2.bmp_press = bmp_press;
		pack2.bmp_humidity = bmp_humidity;
		pack2.bme_height = height;
		pack2.lux = lux;
		pack2.time_ms = HAL_GetTick();
		num2 += 1;
		pack2.num = num2;
		num1 += 1;
		pack1.num = num1;
		pack3.time_ms = HAL_GetTick();
		num3 += 1;
		pack3.num = num3;
		num4 += 1;
		packq.num = num4;
		for (int i = 0; i < 3; i++){
			pack1.accl[i] = acc_g[i]*1000;
			pack1.gyro[i] = gyro[i];
			pack1.mag[i] = mag[i];
		}
		pack2.crc = Crc16((uint8_t *)&pack2, sizeof(pack2) - 2);
		pack1.crc = Crc16((uint8_t *)&pack1, sizeof(pack1) - 2);
		packq.crc = Crc16((uint8_t *)&packq, sizeof(packq) - 2);
		pack3.crc = Crc16((uint8_t *)&pack3, sizeof(pack3) - 2);
 		switch(state_nrf){
		case STATE_GEN_PACK_2:
			nrf24_fifo_flush_tx(&nrf24);
			nrf24_fifo_status(&nrf24, &rx_status, &tx_status);
			nrf24_fifo_write(&nrf24, (uint8_t *)&pack2, sizeof(pack2), true);//32
			//uint8_t pack2_size = sizeof(pack2);
			start_time_nrf = HAL_GetTick();
			state_nrf = STATE_WAIT;
			break;
		case STATE_WAIT:
			nrf24_irq_get(&nrf24, &comp);
			if(comp != 0){///HAL_GPIO_ReadPin(GPIOC, GPIO_PIN_15)== GPIO_PIN_RESET){
				//nrf24_irq_get(&nrf24, &comp);
				nrf24_irq_clear(&nrf24, comp);
				nrf24_fifo_status(&nrf24, &rx_status, &tx_status);
				/*if(tx_status == NRF24_FIFO_EMPTY){
					counter++;
					if(counter == 2){
						state_nrf = STATE_GEN_PACK_2;
						counter = 0;
					}
					else{
						state_nrf = STATE_GEN_PACK_1;
					}
				}*/
			}
			if (HAL_GetTick()-start_time_nrf >= 1)
			{
				nrf24_irq_get(&nrf24, &comp);
				nrf24_fifo_status(&nrf24, &rx_status, &tx_status);
				nrf24_fifo_flush_tx(&nrf24);
				nrf24_fifo_status(&nrf24, &rx_status, &tx_status);
				counter++;
				if(counter == 4 || counter == 7){
					state_nrf = STATE_GEN_PACK_2;
				} else if(counter == 8){
					state_nrf = STATE_GEN_PACK_3;
					counter = 0;
				}
				else{
					state_nrf = STATE_GEN_PACK_1_Q;
				}
			}
			break;
		case STATE_GEN_PACK_1_Q:
			nrf24_fifo_flush_tx(&nrf24);
			its_bme280_read(UNKNOWN_BME, &bme_shit);

			nrf24_fifo_write(&nrf24, (uint8_t *)&pack1, sizeof(pack1), false);
			nrf24_fifo_write(&nrf24, (uint8_t *)&pack1, sizeof(pack1), false);
			//uint8_t pack1_size = sizeof(pack1);
			nrf24_fifo_write(&nrf24, (uint8_t *)&packq, sizeof(packq), false);
			//uint8_t packq_size = sizeof(packq);
			state_nrf = STATE_WAIT;
			break;
		case STATE_GEN_PACK_3:
			nrf24_fifo_flush_tx(&nrf24);
			nrf24_fifo_write(&nrf24, (uint8_t *)&pack3, sizeof(pack3), false);
			//uint8_t pack3_size = sizeof(pack3);
			state_nrf = STATE_WAIT;
			break;
 		}

 		/*printf("%d\n", HAL_GetTick());*/

		if(res1 == FR_OK){
			str_wr = sd_parse_to_bytes_pack1(str_buf, &pack1);
			res1 = f_write(&File1, str_buf, str_wr, &Bytes); // отправка на запись в файл
			res1 = f_sync(&File1);
		}
		if(res2 == FR_OK){
			str_wr = sd_parse_to_bytes_pack2(str_buf, &pack2);
			res2 = f_write(&File2, str_buf, str_wr, &Bytes); // отправка на запись в файл
			res2 = f_sync(&File2);
		}
		if(res3 == FR_OK){
			str_wr = sd_parse_to_bytes_pack3(str_buf, &pack3);
			res3 = f_write(&File3, str_buf, str_wr, &Bytes); // отправка на запись в файл
			res3 = f_sync(&File3);
		}
		if(resb == FR_OK){
			resb = f_write(&Fileb,(uint8_t *)&pack1,sizeof(pack1), &Bytes); // отправка на запись в файл
			resb = f_write(&Fileb,(uint8_t *)&pack2,sizeof(pack2), &Bytes); // отправка на запись в файл
			resb = f_write(&Fileb,(uint8_t *)&pack3,sizeof(pack3), &Bytes); // отправка на запись в файл
			resb = f_write(&Fileb,(uint8_t *)&packq,sizeof(packq), &Bytes); // отправка на запись в файл
			resb = f_sync(&Fileb); // запись в файл (на sd контроллер пишет не сразу, а по закрытии файла. Также можно использовать эту команду)
		}
	}
}

