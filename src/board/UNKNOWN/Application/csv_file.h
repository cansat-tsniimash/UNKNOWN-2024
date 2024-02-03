/*
 * csv_file.h
 *
 *  Created on: Sep 23, 2023
 *      Author: Install
 */

#ifndef CSV_FILE_H_
#define CSV_FILE_H_

#include <string.h>
#include <stdio.h>
#include "structs.h"

uint16_t sd_parse_to_bytes_pack1(char *buffer, pack1_t *pack1);

uint16_t sd_parse_to_bytes_pack2(char *buffer, pack2_t *pack2);

uint16_t sd_parse_to_bytes_pack3(char *buffer, pack3_t *pack3);

uint16_t sd_parse_to_bytes_quaterneon(char *buffer, packq_t *q);

#endif /* CSV_FILE_H_ */
