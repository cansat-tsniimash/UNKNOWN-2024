/*
 * cvs_file.c
 *
 *  Created on: 22 сент. 2023 г.
 *      Author: Install
 */


#include "csv_file.h"



uint16_t sd_parse_to_bytes_pack1(char *buffer, pack1_t *pack1) {
	memset(buffer, 0, 300);
	uint16_t num_written = snprintf(
			buffer, 300,
			"%d;%d;%d;%d;%d;%d;%d;%d;%d;%d;%d\n",
			 pack1->num, pack1->time_ms, pack1->accl[0], pack1->accl[1], pack1->accl[2], pack1->gyro[0], pack1->gyro[1], pack1->gyro[2], pack1->mag[0], pack1->mag[1], pack1->mag[2]);
	return num_written;
}
uint16_t sd_parse_to_bytes_pack2(char *buffer, pack2_t *pack2) {
	memset(buffer, 0, 300);
	uint16_t num_written = snprintf(
			buffer, 300,
			"%d;%d;%d;%d;%d;%f;%f;\n",
			pack2->num, pack2->time_ms, pack2->bmp_temp, pack2->bmp_press, pack2->bmp_humidity, pack2->bme_height, pack2->lux);
	return num_written;
}

uint16_t sd_parse_to_bytes_pack3(char *buffer, pack3_t *pack3) {
	memset(buffer, 0, 300);
	uint16_t num_written = snprintf(
			buffer, 300,
			"%d; %d; %d; %f; %f; %f; %d; %d;\n",
			pack3->num, pack3->time_ms, pack3->fix, pack3->lat, pack3->lon, pack3->alt, pack3->gps_time_s, pack3->gps_time_us);
	return num_written;
}

uint16_t sd_parse_to_bytes_quaterneon(char *buffer, packq_t *q) {
	memset(buffer, 0, 300);
	uint16_t num_written = snprintf(
			buffer, 300,
			"%f	%f	%f	%f	%f\n",
			q->times, q->q1, q->q2, q->q3, q->q4);
	return num_written;
}
