/*
 * strukts.c
 *
 *  Created on: Sep 23, 2023
 *      Author: Install
 */
#include <string.h>
#include <stdio.h>

typedef struct{
	int16_t accl[3];
	int16_t gyro[3];
	int16_t mag[3];
}pack1_t;
typedef struct{
	double bmp_temp;
	double bmp_press;
	double bmp_humidity;
}pack2_t;
