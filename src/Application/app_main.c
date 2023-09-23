/*
 * app_main.c
 *	С НОВЫМ ГОДОМ ЭЩКЕРЕЕ
 *  Created on: Sep 20, 2023
 *      Author: Install
 */
#include "BME280/DriverForBME280.h"
#include "main.h"
#include "Shift_Register/shift_reg.h"
#include <LSM6DS3/DLSM.h>
#include <LIS3MDL/DLIS3.h>
#include <string.h>
#include <stdio.h>
#include "csv_file.h"
#include "structs.h"
#include <fatfs.h>

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
	float temperature_celsius_gyro = 0.0;
	float acc_g[3] = {0};
	float gyro_dps[3] = {0};
	float temperature_celsius_mag = 0.0;
	float mag[3] = {0};
	float lat;
	float lon;
	float alt;
	uint16_t str_wr;
	UINT Bytes;
	char str_buf[300];
	double bmp_temp;
	double bmp_press;
	double bmp_humidity;
	//сдвиговый регистр
	shift_reg_t shift_reg_n;
	shift_reg_n.bus = &hspi1;
	shift_reg_n.latch_port = GPIOC;
	shift_reg_n.latch_pin = GPIO_PIN_1;
	shift_reg_n.oe_port = GPIOC;
	shift_reg_n.oe_pin = GPIO_PIN_13;
	shift_reg_n.value = 0;
	shift_reg_init(&shift_reg_n);
	shift_reg_write_16(&shift_reg_n, 0xFFFF);

	shift_reg_t shift_reg_r;
	shift_reg_r.bus = &hspi1;
	shift_reg_r.latch_port = GPIOC;
	shift_reg_r.latch_pin = GPIO_PIN_4;
	shift_reg_r.oe_port = GPIOC;
	shift_reg_r.oe_pin = GPIO_PIN_5;
	shift_reg_r.value = 0;
	shift_reg_init(&shift_reg_r);
	shift_reg_write_8(&shift_reg_r, 0xFF);
	//работа бме
	struct bme_spi_intf_sr bme_struct;
	bme_struct.sr_pin = 2;
	bme_struct.sr = &shift_reg_n;
	bme_struct.spi = &hspi1;
	struct bme280_dev bme;
	bme_init_default_sr(&bme, &bme_struct);
	struct bme280_data bme_data;
	bme_data = bme_read_data(&bme);
	//стх и структура лcмa
	stmdev_ctx_t ctx_lsm;
	struct lsm_spi_intf_sr lsm_sr;
	lsm_sr.sr_pin = 4;
	lsm_sr.spi = &hspi1;
	lsm_sr.sr = &shift_reg_n;
	lsmset_sr(&ctx_lsm, &lsm_sr);

	//стх и структура лиса
	stmdev_ctx_t ctx_lis;
	struct lis_spi_intf_sr lis_sr;
	lis_sr.sr_pin = 3;
	lis_sr.spi = &hspi1;
	lis_sr.sr = &shift_reg_n;
	lisset_sr(&ctx_lis, &lis_sr);
	pack1_t pack1;
	pack2_t pack2;
	//давление на земле
	//double ground_pressure = bme_data.pressure;
	while(1){
		bme_data = bme_read_data(&bme);
		bmp_temp = bme_data.temperature * 100;
		bmp_press = bme_data.pressure;
		bmp_humidity = bme_data.humidity;

		lsmread(&ctx_lsm, &temperature_celsius_gyro, &acc_g, &gyro_dps);
		lisread(&ctx_lis, &temperature_celsius_mag, &mag);


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
		}
		if(res2 == FR_OK){
			str_wr = sd_parse_to_bytes_pack2(str_buf, &pack2);
			res2 = f_write(&File2, str_buf, str_wr, &Bytes); // отправка на запись в файл
		}

	}
}
