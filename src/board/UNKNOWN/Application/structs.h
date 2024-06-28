/*
 * structs.h
 *
 *  Created on: Sep 23, 2023
 *      Author: Install
 */

#ifndef STRUCTS_H_
#define STRUCTS_H_

#include <string.h>
#include <stdio.h>
#pragma pack(push,1)
// 18
typedef struct{
	uint8_t flag;
	uint16_t num;
	uint32_t time_ms;
	int16_t accl[3]; //6
	int16_t gyro[3]; // 6
	int16_t mag[3];// 6
	uint16_t crc;
}pack1_t;
//11
typedef struct{
	uint8_t flag; // 1
	uint16_t num;
	uint32_t time_ms;
	int16_t bmp_temp; // 2
	uint32_t bmp_press; //4
	int16_t bmp_humidity; // 2
	float bme_height; // 2
	float lux;
	uint8_t state;
	uint16_t crc;
}pack2_t;

typedef struct{
	uint8_t flag; // 1
	uint16_t num;
	uint32_t time_ms;
	int16_t fix;
	float lat;
	float lon;
	float alt;
	uint64_t gps_time_s;
	uint32_t gps_time_us;
	uint16_t crc;
}pack3_t;

typedef struct{
	uint8_t flag; // 1
	uint16_t num;
	uint32_t time_ms;
	float times;
	float q1;
	float q2;
	float q3;
	float q4;
	uint16_t crc;
}packq_t;
#pragma pack(pop)

#endif /* STRUCTS_H_ */
