#include <iostream>

int func(int a, int b, int c) {
    int result = a / b;
    return result;
}

int main() {
    int c = 29;
    int a = 46;
    int b = 59;

    std::cout << "result: " << func(a,c);

    return 0;
}