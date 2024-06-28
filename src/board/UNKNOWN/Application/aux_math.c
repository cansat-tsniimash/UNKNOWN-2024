#include <math.h>

#include "Quaternion.h"


#define WGS84_A 6378136.5
#define WGS84_B 6356751.758



void latlon_to_cartesian(double lat_rad, double lon_rad, double alt_m, double * xyz_m)
{
	double lat = lat_rad;
	double lon = lon_rad;
	double alt = alt_m;
	lat = lat * M_PI / 180.0;
	lon = lon * M_PI / 180.0;
	const double b2da2 = (WGS84_B*WGS84_B)/(WGS84_A*WGS84_A);
	const double nb = (WGS84_A*WGS84_A)/sqrt((WGS84_A*WGS84_A) * cos(lat)*cos(lat) + (WGS84_B*WGS84_B) * sin(lat) * sin(lat));
	double x_gps = (nb + alt)* cos(lat) * cos(lon);
	double y_gps = (nb + alt)* cos(lat) * sin(lon);
	double z_gps = (b2da2*nb + alt) * sin(lat);
	xyz_m[0] = x_gps;
	xyz_m[1] = y_gps;
	xyz_m[2] = z_gps;
}


void quat_vec_mul(const float * quat, const double * vec_in, double * vec_out)
{
	Quaternion q = {
		.w = quat[0],
		.v = {quat[1], quat[2], quat[3]}
	};

	Quaternion_rotate(&q, (double*)vec_in, vec_out);
}


void mag_cal_values(const float raws[3], float out[3])
{
	const double bx = -0.145156;
	const double by = -0.816267;
	const double bz = -0.981632;

	const double xx = 2.385585;
	const double xy = -0.181853;
	const double xz = -0.380441;

	const double yy = 2.270106;
	const double yz = -0.537272;

	const double zz = 1.220646;

	const double braws[3] = {
		raws[0] - bx,
		raws[1] - by,
		raws[2] - bz,
	};

	double rv[3];
	out[0] = braws[0] * xx + braws[1] * xy + braws[2] * xz;
	out[1] = braws[0] * xy + braws[1] * yy + braws[2] * yz;
	out[2] = braws[0] * xz + braws[1] * yz + braws[2] * zz;
}
