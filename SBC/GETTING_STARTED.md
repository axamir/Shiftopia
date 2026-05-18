# شروع کار با فورک بیتکوین (برای توسعه‌دهندگان)

## پیش‌نیازها
- آشنایی با C++ (هسته بیتکوین به زبان C++ است)
- دانش پایه از رمزنگاری و الگوریتم‌های اجماع
- نصب Git, CMake, و کتابخانه‌های مورد نیاز بیتکوین

## گام ۱: فورک کردن مخزن بیتکوین
```bash
git clone https://github.com/bitcoin/bitcoin.git shiftopia-bitcoin
cd shiftopia-bitcoin
./autogen.sh
./configure --with-incompatible-bdb --enable-debug
make
src/bitcoind -testnet



گام ۵: ایجاد پل با بیتکوین واقعی (پیشرفته)

از کتابخانه‌های موجود مانند libwally یا rust-bitcoin برای ارتباط با بیتکوین استفاده کنید.

نیاز به کمک؟

در گفتگوی کافه نقطه صفر موضوع را مطرح کنید.
