#include <avr/io.h>
#include <util/delay.h>

void init_serial() {
    UBRR0H = 0;
    UBRR0L = 103; // 9600 baud rate
    UCSR0B = (1 << TXEN0) | (1 << RXEN0);
}

void send_serial_data(uint8_t data) {
    while (!(UCSR0A & (1 << UDRE0)));
    UDR0 = data;
}

uint8_t receive_serial_data() {
    while (!(UCSR0A & (1 << RXC0)));
    return UDR0;
}

int main() {
    init_serial();
    
    while (1) {
        uint8_t data = receive_serial_data();
        send_serial_data(data); // Echo received data back to Raspberry Pi
    }
}
