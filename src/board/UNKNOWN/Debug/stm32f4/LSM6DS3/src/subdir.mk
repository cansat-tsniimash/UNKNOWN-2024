################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (9-2020-q2-update)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
C:/Users/Install/Documents/git/KNPN-2023/lib-tsniimash/stm32f4/LSM6DS3/src/DLSM.c \
C:/Users/Install/Documents/git/KNPN-2023/lib-tsniimash/stm32f4/LSM6DS3/src/lsm6ds3_reg.c 

OBJS += \
./stm32f4/LSM6DS3/src/DLSM.o \
./stm32f4/LSM6DS3/src/lsm6ds3_reg.o 

C_DEPS += \
./stm32f4/LSM6DS3/src/DLSM.d \
./stm32f4/LSM6DS3/src/lsm6ds3_reg.d 


# Each subdirectory must supply rules for building sources it contributes
stm32f4/LSM6DS3/src/DLSM.o: C:/Users/Install/Documents/git/KNPN-2023/lib-tsniimash/stm32f4/LSM6DS3/src/DLSM.c stm32f4/LSM6DS3/src/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m4 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32F411xE -c -I../Drivers/CMSIS/Include -I../Core/Inc -I../Drivers/STM32F4xx_HAL_Driver/Inc -I../Drivers/CMSIS/Device/ST/STM32F4xx/Include -I../Drivers/STM32F4xx_HAL_Driver/Inc/Legacy -I"C:/Users/Install/Documents/git/KNPN-2023/lib-tsniimash/stm32f4" -I../FATFS/Target -I../FATFS/App -I../Middlewares/Third_Party/FatFs/src -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -o "$@"
stm32f4/LSM6DS3/src/lsm6ds3_reg.o: C:/Users/Install/Documents/git/KNPN-2023/lib-tsniimash/stm32f4/LSM6DS3/src/lsm6ds3_reg.c stm32f4/LSM6DS3/src/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m4 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32F411xE -c -I../Drivers/CMSIS/Include -I../Core/Inc -I../Drivers/STM32F4xx_HAL_Driver/Inc -I../Drivers/CMSIS/Device/ST/STM32F4xx/Include -I../Drivers/STM32F4xx_HAL_Driver/Inc/Legacy -I"C:/Users/Install/Documents/git/KNPN-2023/lib-tsniimash/stm32f4" -I../FATFS/Target -I../FATFS/App -I../Middlewares/Third_Party/FatFs/src -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-stm32f4-2f-LSM6DS3-2f-src

clean-stm32f4-2f-LSM6DS3-2f-src:
	-$(RM) ./stm32f4/LSM6DS3/src/DLSM.d ./stm32f4/LSM6DS3/src/DLSM.o ./stm32f4/LSM6DS3/src/lsm6ds3_reg.d ./stm32f4/LSM6DS3/src/lsm6ds3_reg.o

.PHONY: clean-stm32f4-2f-LSM6DS3-2f-src

