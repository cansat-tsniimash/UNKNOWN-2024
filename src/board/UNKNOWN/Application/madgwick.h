/*
 * pomelo.h
 *
 *  Created on: 31 янв. 2024 г.
 *      Author: Install
 */

#ifndef MADGWICK_H_
#define MADGWICK_H_

void MadgwickAHRSupdate(float* quaternion, float gx, float gy, float gz, float ax, float ay, float az, float mx, float my, float mz, float dt, float beta);// beta = 0,3
void MadgwickAHRSupdateIMU(float* quaternion, float gx, float gy, float gz, float ax, float ay, float az, float dt, float beta);

#endif /* POMELO_H_ */
