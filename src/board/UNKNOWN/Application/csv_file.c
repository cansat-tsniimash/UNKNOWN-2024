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
			"%d;%d;%d;%d;%d;%d;%d;%d;%d\n",
			pack1->accl[0], pack1->accl[1], pack1->accl[2], pack1->gyro[0], pack1->gyro[1], pack1->gyro[2], pack1->mag[0], pack1->mag[1], pack1->mag[2]);
	return num_written;
}
uint16_t sd_parse_to_bytes_pack2(char *buffer, pack2_t *pack2) {
	memset(buffer, 0, 300);
	uint16_t num_written = snprintf(
			buffer, 300,
			"%d;%d;%d;\n",
			pack2->bmp_temp, pack2->bmp_press, pack2->bmp_humidity);
	return num_written;
}
