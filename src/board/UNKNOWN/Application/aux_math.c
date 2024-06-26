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
