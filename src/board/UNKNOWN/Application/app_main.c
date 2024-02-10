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

extern SPI_HandleTypeDef hspi5;
extern SPI_HandleTypeDef hspi1;
extern UART_HandleTypeDef huart1;
extern SPI_HandleTypeDef hspi4;
extern I2C_HandleTypeDef hi2c1;
extern ADC_HandleTypeDef hadc1;


int _write(int file, char *ptr, int len)
{
HAL_UART_Transmit(&huart1, (uint8_t *)ptr, len, 100);
return 0;
}

typedef enum
{
	STATE_GEN_PACK_1 = 1,
	STATE_WAIT = 2,
	STATE_GEN_PACK_2_Q = 3,
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


int app_main(){
	//файлы
	FATFS fileSystem; // переменная типа FATFS
	FIL File1; // хендлер файла
	FIL File2;
	FIL File3;
	FIL File4;
	FIL Fileq;
	FIL File_bin;
	FRESULT res1 = 255;
	FRESULT res2 = 255;
	FRESULT res3 = 255;
	FRESULT res4 = 255;
	FRESULT resq = 255;
	FRESULT res_bin = 255;
	FRESULT megares = 255;
	const char path1[] = "packet1.csv";
 	const char path2[] = "packet2.csv";
 	const char path3[] = "packet3.csv";
 	const char pathq[] = "quaternion.csv";
	memset(&fileSystem, 0x00, sizeof(fileSystem));
	FRESULT is_mount = 0;
	extern Disk_drvTypeDef disk;
	disk.is_initialized[0] = 0;
	is_mount = f_mount(&fileSystem, "", 1);
	if(is_mount == FR_OK) { // монтируете файловую систему по пути SDPath, проверяете, что она смонтировалась, только при этом условии начинаете с ней работать
		res1 = f_open(&File1, (char*)path1, FA_WRITE | FA_CREATE_ALWAYS); // открытие файла, обязательно для работы с ним
		f_puts("accl1; accl2; accl3; gyro1; gyro2; gyro3; mag1; mag2; mag\n;", &File1);
		res1 = f_sync(&File1);
	}
	if(is_mount == FR_OK) { // монтируете файловую систему по пути SDPath, проверяете, что она смонтировалась, только при этом условии начинаете с ней работать
		res2 = f_open(&File2, (char*)path2, FA_WRITE | FA_CREATE_ALWAYS); // открытие файла, обязательно для работы с ним
		f_puts("bmp_temp; bmp_press; bmp_humidity; bmp_height; photorez\n", &File2);
		res2 = f_sync(&File2);
	}
	if(is_mount == FR_OK) { // монтируете файловую систему по пути SDPath, проверяете, что она смонтировалась, только при этом условии начинаете с ней работать
		res3 = f_open(&File3, (char*)path3, FA_WRITE | FA_CREATE_ALWAYS); // открытие файла, обязательно для работы с ним
		f_puts("lat; lon; alt; times; timems\n", &File3);
		res3 = f_sync(&File3);
	}
	if(is_mount == FR_OK) { // монтируете файловую систему по пути SDPath, проверяете, что она смонтировалась, только при этом условии начинаете с ней работать
		resq = f_open(&Fileq, (char*)pathq, FA_WRITE | FA_CREATE_ALWAYS); // открытие файла, обязательно для работы с ним
		f_puts("", &Fileq);
		resq = f_sync(&Fileq);
	}

	//переменные
	uint8_t counter = 0;
	state_nrf_t state_nrf;
	state_nrf = STATE_GEN_PACK_1;
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

	uint32_t start_time_par = 0;
	uint32_t start_time_stab = 0;
	float time_now = 0;
	float time_before = 1;
	float alt;
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
	shift_reg_r.latch_pin = GPIO_PIN_2;
	shift_reg_r.oe_port = GPIOB;
	shift_reg_r.oe_pin = GPIO_PIN_10;
	shift_reg_r.value = 0;
	shift_reg_init(&shift_reg_r);
	shift_reg_write_8(&shift_reg_r, 0xFF);
	state_t state_now;
	state_now = STATE_READY;
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
	lsm_sr.sr_pin = 4;
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

	nrf24_mode_power_down(&nrf24);
	nrf24_rf_config_t nrf_config;
	nrf_config.data_rate = NRF24_DATARATE_250_KBIT;
	nrf_config.tx_power = NRF24_TXPOWER_MINUS_18_DBM;
	nrf_config.rf_channel = 101;
	nrf24_setup_rf(&nrf24, &nrf_config);
	nrf24_protocol_config_t nrf_protocol_config;
	nrf_protocol_config.crc_size = NRF24_CRCSIZE_1BYTE;
	nrf_protocol_config.address_width = NRF24_ADDRES_WIDTH_5_BYTES;
	nrf_protocol_config.en_dyn_payload_size = false;
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
	nrf24_mode_tx(&nrf24);
	//gps
	gps_init();
	__HAL_UART_ENABLE_IT(&huart1, UART_IT_RXNE);
	__HAL_UART_ENABLE_IT(&huart1, UART_IT_ERR);
	uint32_t gps_time_s;
	uint32_t gps_time_us;
	//стх и структура лиса
	stmdev_ctx_t ctx_lis;
	struct lis_spi_intf_sr lis_sr;
	lis_sr.sr_pin = 1;
	lis_sr.spi = &hspi1;
	lis_sr.sr = &shift_reg_r;
	lisset_sr(&ctx_lis, &lis_sr);

	pack1_t pack1;
	pack2_t pack2;
	pack3_t pack3;
	packq_t packq;
	pack1.flag = 0xBB;
	pack2.flag = 0xAA;
	pack3.flag = 0xCC;
	packq.flag = 0xFF;
	//давление на земле
	its_bme280_read(UNKNOWN_BME, &bme_shit);
	double ground_pressure = bme_shit.pressure;
	bmp_temp = bme_shit.temperature * 100;
	bmp_press = bme_shit.pressure;
	bmp_humidity = bme_shit.humidity;
	uint32_t height = 44330 * (1 - pow(bmp_press / ground_pressure, 1.0 / 5.255));
	uint32_t ground_height = 44330 * (1 - pow(bmp_press / ground_pressure, 1.0 / 5.255));
	ground_height += 30;
	while(1){
		//bme280
		bmp_temp = bme_shit.temperature * 100;
		bmp_press = bme_shit.pressure;
		bmp_humidity = bme_shit.humidity;
		height = 44330 * (1 - pow(bmp_press / ground_pressure, 1.0 / 5.255));
		//сдвиговый регистр
		shift_reg_write_bit_8(&shift_reg_r, 3, 1);
		float lux = photorezistor_get_lux(photrez);
		//gps
		gps_work();
		gps_get_coords(&cookie, &lat, &lon, &alt, &fix_);
		gps_get_time(&cookie, &gps_time_s, &gps_time_us);
		//lsm и lis
		lsmread(&ctx_lsm, &temperature_celsius_gyro, &acc_g, &gyro_dps);
		lisread(&ctx_lis, &temperature_celsius_mag, &mag);
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
		MadgwickAHRSupdate(seb_quaternion, gyro_m[0], gyro_m[1], gyro_m[2], acc_m[0], acc_m[1], acc_m[2], mag[0], mag[1], mag[2], time_before-time_now, 0.3);
		/*MadgwickAHRSupdateIMU(seb_quaternion, gyro_m[0], gyro_m[1], gyro_m[2], acc_m[0], acc_m[1], acc_m[2], time_before-time_now, 0.3);*/
		time_before = time_now;
		printf("%f	%f	%f	%f	%f\n", time_now, seb_quaternion[0], seb_quaternion[1], seb_quaternion[2], seb_quaternion[3]);
		/*printf("%f	%f	%f\n", gyro_dps[0], gyro_dps[1], gyro_dps[2]);*/
		packq.times = time_now;
		packq.q1 = seb_quaternion[0];
		packq.q2 = seb_quaternion[1];
		packq.q3 = seb_quaternion[2];
		packq.q4 = seb_quaternion[3];
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



		switch (state_now)
				{
				case STATE_READY:
					//HAL_Delay(100);
					if(0/*HAL_GPIO_ReadPin(GPIOx, GPIO_PIN_x)*/){
						state_now = STATE_IN_ROCKET;
						limit_lux = lux * 0.8;
					}
					break;
				case STATE_IN_ROCKET:
					if(lux >=  limit_lux){
						state_now = STATE_AFTER_ROCKET;
						break;
					}

					break;
				case STATE_AFTER_ROCKET:
					start_time_par = HAL_GetTick();
					if (HAL_GetTick()-start_time_par >= 3228)
					{
						state_now = STATE_STABILZATORS;
						break;
					}
				case STATE_STABILZATORS:
					shift_reg_write_bit_8(&shift_reg_r, 2, 1);
					start_time_stab = HAL_GetTick();
					if (HAL_GetTick()-start_time_par >= 1488)
					{
						state_now = STATE_DESCENT;
						break;
					}
				case STATE_DESCENT:
					//наведение
					if(height <= ground_height){
						state_now = STATE_ON_EARTH;
						break;
					}
				case STATE_ON_EARTH:
					//ыкл камеры и вкл пищалки
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

 		switch(state_nrf){
		case STATE_GEN_PACK_1:
			nrf24_fifo_flush_tx(&nrf24);
			nrf24_fifo_write(&nrf24, (uint8_t *)&pack1, 32, false);//32
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
			if (HAL_GetTick()-start_time_nrf >= 100)
			{
				nrf24_irq_get(&nrf24, &comp);
				nrf24_fifo_status(&nrf24, &rx_status, &tx_status);
				nrf24_fifo_flush_tx(&nrf24);
				nrf24_fifo_status(&nrf24, &rx_status, &tx_status);
				counter++;
				if(counter == 2){
					state_nrf = STATE_GEN_PACK_1;
					counter = 0;
				}
				else{
					state_nrf = STATE_GEN_PACK_2_Q;
				}
			}
			break;
		case STATE_GEN_PACK_2_Q:
			nrf24_fifo_flush_tx(&nrf24);
			nrf24_fifo_write(&nrf24, (uint8_t *)&pack2, sizeof(pack2), false);
			nrf24_fifo_write(&nrf24, (uint8_t *)&packq, sizeof(packq), false);
			state_nrf = STATE_WAIT;
			break;
		case STATE_GEN_PACK_3:
			nrf24_fifo_flush_tx(&nrf24);
			nrf24_fifo_write(&nrf24, (uint8_t *)&pack3, sizeof(pack3), false);
			state_nrf = STATE_WAIT;
			break;
 		/*printf("%d\n", HAL_GetTick());*/
		pack2.bmp_temp = bmp_temp;
		pack2.bmp_press = bmp_press;
		pack2.bmp_humidity = bmp_humidity;
		pack2.bme_height = height;
		pack2.lux = lux;
		for (int i = 0; i < 3; i++){
			pack1.accl[i] = acc_g[i]*1000;
			pack1.gyro[i] = gyro_dps[i]*1000;
			pack1.mag[i] = mag[i]*1000;
		}
		/*if(res1 == FR_OK){
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
		printf("%d\n", HAL_GetTick());*/

	}
}
