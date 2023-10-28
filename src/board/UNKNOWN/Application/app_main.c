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

extern SPI_HandleTypeDef hspi5;
extern SPI_HandleTypeDef hspi1;
extern UART_HandleTypeDef huart1;
extern SPI_HandleTypeDef hspi4;

typedef enum
{
	STATE_GEN_PACK_1 = 1,
	STATE_WAIT = 2,
	STATE_GEN_PACK_2 = 3,
} state_nrf_t;


int app_main(){
	//файлы
	FATFS fileSystem; // переменная типа FATFS
	FIL File1; // хендлер файла
	FIL File2;
	FIL File_bin;
	FRESULT res1 = 255;
	FRESULT res2 = 255;
	FRESULT res_bin = 255;
	FRESULT megares = 255;
	const char path1[] = "packet1.csv";
 	const char path2[] = "packet2.csv";
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
		f_puts("bmp_temp; bmp_press; bmp_humidity\n", &File2);
		res2 = f_sync(&File2);
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
	float lat;
	float lon;
	float alt;
	int fix_;
	int comp = 0;
	int64_t cookie;
	uint16_t str_wr;
	UINT Bytes;
	char str_buf[300];
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
	//стх и структура лcмa
	stmdev_ctx_t ctx_lsm;
	struct lsm_spi_intf_sr lsm_sr;
	lsm_sr.sr_pin = 4;
	lsm_sr.spi = &hspi1;
	lsm_sr.sr = &shift_reg_r;
	lsmset_sr(&ctx_lsm, &lsm_sr);


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
	uint64_t gps_time_s;
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
	pack1.flag = 0xBB;
	pack2.flag = 0xAA;
	//давление на земле
	//double ground_pressure = bme_data.pressure;
	while(1){
		//bme_data = bme_read_data(&bme);
		//bmp_temp = bme_data.temperature * 100;
		//bmp_press = bme_data.pressure;
		//bmp_humidity = bme_data.humidity;
		its_bme280_read(UNKNOWN_BME, &bme_shit);
		bmp_temp = bme_shit.temperature * 100;
		bmp_press = bme_shit.pressure;
		bmp_humidity = bme_shit.humidity;

		shift_reg_write_bit_8(&shift_reg_r, 3, 1);


		gps_work();
		gps_get_coords(&cookie, &lat, &lon, &alt, &fix_);
		gps_get_time(&cookie, &gps_time_s, &gps_time_us);




		lsmread(&ctx_lsm, &temperature_celsius_gyro, &acc_g, &gyro_dps);
		lisread(&ctx_lis, &temperature_celsius_mag, &mag);

 		switch(state_nrf){
		case STATE_GEN_PACK_1:
			nrf24_fifo_flush_tx(&nrf24);
			nrf24_fifo_write(&nrf24, (uint8_t *)&pack1, 32, false);//32
			state_nrf = STATE_WAIT;
			break;
		case STATE_WAIT:
			if(HAL_GPIO_ReadPin(GPIOC, GPIO_PIN_15)== GPIO_PIN_RESET){
				nrf24_irq_get(&nrf24, &comp);
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
				nrf24_fifo_status(&nrf24, &rx_status, &tx_status);
				nrf24_fifo_flush_tx(&nrf24);
				nrf24_fifo_status(&nrf24, &rx_status, &tx_status);
				counter++;
				if(counter == 2){
					state_nrf = STATE_GEN_PACK_1;
					counter = 0;
				}
				else{
					state_nrf = STATE_GEN_PACK_1;
				}
			}
			break;
		case STATE_GEN_PACK_2:
			nrf24_fifo_flush_tx(&nrf24);
			nrf24_fifo_write(&nrf24, (uint8_t *)&pack2, sizeof(pack2), false);
			state_nrf = STATE_WAIT;
			break;
		}
		pack2.bmp_temp = bmp_temp;
		pack2.bmp_press = bmp_press;
		pack2.bmp_humidity = bmp_humidity;
		for (int i = 0; i < 3; i++){
			pack1.accl[i] = acc_g[i]*1000;
			pack1.gyro[i] = gyro_dps[i]*1000;
			pack1.mag[i] = mag[i]*1000;
		}
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

	}
}
