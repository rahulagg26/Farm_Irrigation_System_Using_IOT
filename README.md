# Farm_Irrigation_System_Using_IOT
The programme to display the value of the sensors, which is mentioned in display.py file

### As per our implementation, we have created three python files to establish the required communication between the system and the **Raspberry Pi**. The use of three different python files.

1. **subscriber.py**: This file is present on our system (laptop), where in the first case we are acting as a subscriber, and in the second case we are acting as a publisher.

2. **publisher.py**: This file is present on our Raspberry Pi, where we are publishing the temperature and humidity values.

3. **subscriber-raspPi.py**: This file is also present on our Raspberry Pi where we are acting as a subscriber to receive the predicted value of water percentage from the publisher with the help of an ML model.

### Eventually, to display the predicted water percentage in LCD, which is calculated via the ML Model, we have designed the code file **main.py** with the required configuration.
