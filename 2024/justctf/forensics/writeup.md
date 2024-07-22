## Baby SoC

We found really funny device. It was broken from the beginning, trust us! Can you help with recovering the truth?

https://s3.cdn.justctf.team/8bd5f085-5972-4833-af88-df915284fbd6/flashdump.bin

https://github.com/tenable/esp32_image_parser



esp-idf: v4.4.5 ac5d805d0e
arduino-lib-builder
Jun 12 2023
v4.4.5
here
        <!DOCTYPE html>
        <html>
        <head>
            <title>ESP32 Web Server</title>
        </head>
        <body>
            <h1>Hello from ESP32!</h1>
            <form action="/" method="POST">
                <label for="password">Enter Password:</label>
                <input type="text" id="password" name="password"><br><br>
                <input type="submit" value="Submit">
            </form>
    
here2
<h2>Flag: 
</h2>
</body></html>
text/html
got password
we are unlocked!
stillnotaflaglol
Access Point started
IP address: 
HTTP server started

spinlock_acquire
/IDF/components/esp_hw_support/hw_random.c
esp_fill_random
!((vd->flags&VECDESC_FL_SHARED)&&(vd->flags&VECDESC_FL_NONSHARED))
/IDF/components/esp_hw_support/intr_alloc.c
svd != NULL
esp_intr_disable
esp_intr_free
is_vect_desc_usable
find_desc_for_source
system_api
E (%u) %s: Base MAC address is NULL
E (%u) %s: Base MAC must be a unicast MAC
(size_bits % 8) == 0
/IDF/components/esp_hw_support/mac_addr.c
E (%u) %s: Base MAC address from BLK0 of EFUSE CRC error, efuse_crc = 0x%02x; calc_crc = 0x%02x
E (%u) %s: mac address param is NULL
E (%u) %s: mac type is incorrect
esp_efuse_mac_get_default
"(Cannot use REG_CLR_BIT for DPORT registers use DPORT_REG_CLR_BIT)" && (!((((rtc_io_desc[rtcio_num].reg)) >= 0x3ff00000) && ((rtc_io_desc[rtcio_num].reg)) <= 0x3ff13FFC))
rtcio_ll_force_hold_disable
slowclk_cycles < 32767
/IDF/components/esp_hw_support/port/esp32/rtc_time.c
rtc_time
E (%u) %s: slowclk_cycles value too large, possible overflow
E (%u) %s: rtc_time_get() 32kHz xtal has been stopped
E (%u) %s: 32kHz xtal has been stopped
rtc_clk_cal_internal
Unhandled interrupt %d on cpu %d!

ESP_ERR_NVS_VALUE_TOO_LONG
ESP_ERR_NVS_PART_NOT_FOUND
ESP_ERR_NVS_NEW_VERSION_FOUND
ESP_ERR_NVS_XTS_ENCR_FAILED
ESP_ERR_NVS_XTS_DECR_FAILED
ESP_ERR_NVS_XTS_CFG_FAILED
ESP_ERR_NVS_XTS_CFG_NOT_FOUND
ESP_ERR_NVS_ENCR_NOT_SUPPORTED
ESP_ERR_NVS_KEYS_NOT_INITIALIZED
ESP_ERR_NVS_CORRUPT_KEY_PART
ESP_ERR_NVS_CONTENT_DIFFERS
ESP_ERR_NVS_WRONG_ENCRYPTION
ESP_ERR_ULP_BASE
ESP_ERR_ULP_SIZE_TOO_BIG
ESP_ERR_ULP_INVALID_LOAD_ADDR
ESP_ERR_ULP_DUPLICATE_LABEL

locale::facet::_S_create_c_locale name not valid
iostream
iostream error
Unknown error
St12system_error
A?I,A?(
A?NSt8ios_base7failureB5cxx11E
A?h,A?\,A?
@cannot create shim for unknown locale::facet
uninitialized __any_string
/builds/idf/crosstool-NG/.build/HOST-x86_64-w64-mingw32/xtensa-esp32-elf/src/newlib/newlib/libc/stdlib/btowc.c
@/builds/idf/crosstool-NG/.build/HOST-x86_64-w64-mingw32/xtensa-esp32-elf/src/newlib/newlib/libc/stdlib/wctob.c
blank
@Infinity
/builds/idf/crosstool-NG/.build/HOST-x86_64-w64-mingw32/xtensa-esp32-elf/src/newlib/newlib/libc/stdlib/dtoa.c
Balloc succeeded
/builds/idf/crosstool-NG/.build/HOST-x86_64-w64-mingw32/xtensa-esp32-elf/src/newlib/newlib/libc/stdlib/gdtoa-gethex.c
@?PEA?
/builds/idf/crosstool-NG/.build/HOST-x86_64-w64-mingw32/xtensa-esp32-elf/src/newlib/newlib/libc/stdlib/mprec.c
[%Co
O8M2
vH7B
W4vC
@0000000000000000                
@0000000000000000                0
wifi ipc: failed to post wifi task
failed to post event=%d ret=%d
wifi stop stage3: out of memory!
wifi stop stage2: out of memory!
wifi stop: out of memory!
wifi deinit internal: wifi not stop
alloc net80211 funcs fail
MIC mismatch for the Bcast Mgmt frame(res=%d)
MIC computation for BIP Failed(res=%d)
BIP replay detected
Invalid MMIE
MIC mismatch for the Bcast Mgmt frame(res=%d)
MIC computation for BIP Failed(res=%d)
BIP replay detected
Invalid MMIE

age_reorder: null rap
%s %d
%s %d
%s %d
%s %d
rxa_eb mem fail tid=%d
rap mem fail tid=%d
%s %d
failed to start addba timer
addba index: unknow conn=%p
tap to index: null conn
tap to index: null bss
addba response cb: status %d not success, no need to configure hardware
addba response cb: ap bss deleted
addba response cb: ap conn deleted
addba response cb: bssid change from %02x:%02x:%02x:%02x:%02x:%02x to %02x:%02x:%02x:%02x:%02x:%02x
addba response cb: sta bss deleted
addba response cb: sta conn deleted
addba response invalid param

lloc challenge: out of memory!
%s %d
ioctl_process: invalid arg
invalid ipc cfg
wpa2 ent enable, invalid param(%p)
wifi stop stage error, stage=%d
In function %s, fail to register function!
invalid core id %d
rx ba window %d error
management short buf number %d is out of range
tx buf type %d error
dynamic tx buf number %d is out of range
static tx buf number %d is out of range
dynamic rx buf number %d is out of range
static rx buf number %d is out of range
wpa crypto funcs expected size=%d version=%d, actual size=%d version=%d
invalid magic number %x, call WIFI_INIT_CONFIG_DEFAULT to init config
parameter config should not be NULL
%s %d
%s %d
%s %d
%s %d
%s %d
%s %d
sta is connecting, return error
init nvs: failed, ret=%x
wifi nvs cfg alloc out of memory
nvs invalid min %d max %d
invalid wifi nvs key index %d

	@8*
	@Stack smashing protect failure!
Tasks currently running:
CPU 0/1
CPU 1
CPU 0
Hl`dhTX\480<LPptx|
E (%u) %s: Core dump write binary failed with error=%d
esp_core_dump_common
E (%u) %s: Incorrect size of core dump image: %d
E (%u) %s: Failed to read core dump data size (%d)!
E (%u) %s: Too small core dump partition!
E (%u) %s: No core dump partition found!
E (%u) %s: Core dump data check failed:
E (%u) %s: Failed to read checksum from core dump (%d)!
E (%u) %s: Failed to read data from core dump (%d)!
E (%u) %s: Invalid flash partition config!
E (%u) %s: Core dump flash config is corrupted! CRC=0x%x instead of 0x%x

E (%u) %s: Failed to flush cached data to flash (%d)!
E (%u) %s: Failed to flush cached data to flash (%d)!
E (%u) %s: Failed to erase flash (%d)!
E (%u) %s: Not enough space to save core dump!
E (%u) %s: Failed to write data to flash (%d)!
E (%u) %s: Failed to write cached data to flash (%d)!
E (%u) %s: No core dump partition found!
esp_core_dump_flash
E (%u) %s: Failed to end core dump (%d)!
E (%u) %s: Failed to write core dump header (%d)!
E (%u) %s: Failed to start core dump (%d)!
E (%u) %s: Failed to prepare core dump storage (%d)!
E (%u) %s: %s(%u): Invalid input data.
E (%u) %s: %s(%u): Version info writing failed. Returned (%d).
E (%u) %s: %s(%u): memory regions writing error, returned (%d).
E (%u) %s: %s(%u): ELF Size writing error, returned (%d).
E (%u) %s: %s(%u): ELF header writing error, returned (%d).
E (%u) %s: %s(%u): ELF header writing error, returned (%d).
E (%u) %s: %s(%u): EXTRA_INFO note segment processing failure, returned(%d).
E (%u) %s: %s(%u): Extra info note write failed. Returned (%d).
E (%u) %s: Zero size extra info!
E (%u) %s: %s(%u): Version info note write failed. Returned (%d).
E (%u) %s: %s(%u): memory region write failed. Returned (%d).
E (%u) %s: %s(%u): invalid memory region
E (%u) %s: %s(%u): Interrupted task stack write failed, return (%d).
E (%u) %s: %s(%u): Task %x, TCB write failed, return (%d).
E (%u) %s: %s(%u): Tasks regs addition failed, return (%d).
E (%u) %s: %s(%u): Task %x, stack write failed, return (%d).
E (%u) %s: %s(%u): Task %x, TCB write failed, return (%d).
E (%u) %s: %s(%u): PR_STATUS note segment processing failure, returned(%d).
E (%u) %s: %s(%u): Task %x, PR_STATUS write failed, return (%d).
E (%u) %s: %s(%u): Task %x, PR_STATUS write failed, return (%d).
E (%u) %s: %s(%u): Task %x, PR_STATUS write failed, return (%d).
E (%u) %s: %s(%u): Task %x, PR_STATUS write failed, return (%d).
E (%u) %s: %s(%u): NOTE segment header write failure, returned (%d).
E (%u) %s: Task (TCB:%x), (Stack:%x), stack processing failure = %d.
E (%u) %s: Task (TCB:%x) processing failure = %d

E (%u) %s: Zero size register dump for task 0x%x!
E (%u) %s: %s(%u): Write ELF note data failure, returned (%d)
E (%u) %s: %s(%u): Invalid data pointer for segment
E (%u) %s: %s(%u): Write ELF note data failure (%d)
E (%u) %s: %s(%u): Write ELF note name failure (%d)
E (%u) %s: %s(%u): Write ELF note header failure (%d)
E (%u) %s: %s(%u): Segment note name is too long %d.
E (%u) %s: %s(%u): Write ELF segment data failure (%d)
E (%u) %s: %s(%u): Write ELF segment data failure (%d)
E (%u) %s: %s(%u): Invalid data for segment.
E (%u) %s: %s(%u): Write ELF segment header failure (%d)
E (%u) %s: %s(%u): Write ELF header failure (%d)
esp_core_dump_elf
E (%u) %s: Error while registers processing.
E (%u) %s: Too small stack to keep frame: %d bytes!
esp_core_dump_port
%08x
%s='
E (%u) %s: Empty data to add to checksum calculation!
esp_core_dump_checksum
[%u] %s %u
[%u] CO: create fwn mutex error!
[%u] %s %u
[%u] CO: init coex schm error!
[%u] CO: create bb reset mutex error!
[%u] CO: create semaphore error!
[%u] Error! Should enable WiFi modem sleep when both WiFi and Bluetooth are enabled!!!!!!
[%u] %s %u
						
[%u] CO: create schm semaphore error!
[%u] %s %u
[%u] %s %u
[%u] %s %u
[%u] Coex arbit init: no memory!
[%u] CO: create arbit mux error!
[%u] CO: create arbit mem mux error!
[%u] %s %u
