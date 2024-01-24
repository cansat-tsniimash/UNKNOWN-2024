/*
 * strukts.c
 *
 *  Created on: Sep 23, 2023
 *      Author: Install
 */
#include <string.h>
#include <stdio.h>
// 18
typedef struct{
	uint8_t flag;
	int16_t accl[3]; //6
	int16_t gyro[3]; // 6
	int16_t mag[3];// 6
}pack1_t;
//11
typedef struct{
	uint8_t flag; // 1
	int16_t bmp_temp; // 2
	uint32_t bmp_press; //4
	int16_t bmp_humidity; // 2
	float bme_height; // 2
}pack2_t;
