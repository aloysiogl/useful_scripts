# Installing Windows 10 to an external drive without a Windows host

Original [source](https://gist.github.com/AldoMX/fccd8f7285f8905d71613f12dfa1d714#file-win10-install-to-external-hdd-using-winpe-md)

## The long story

We were talking at the office about having a LAN Party and playing some old
school games like Age of Empires and Starcraft. The issue is that I have Linux
installed. I didn't want to ruin everyone else's fun by having random crashes,
out-of-sync errors and similar stuff using Wine, and I didn't want to do the
dual boot dance, so I figured out that the best option was to install Windows to
an external drive.

I remember that something called [Windows To Go][1] existed a while ago, but it
was restricted to Enterprise versions. Eventually I found out that creating a
Windows To Go drive is a really straightforward process:

1. Partition the External Drive and format it as NTFS.
2. Expand the Windows image using `dism`.
3. Install BOOTMGR using `bcdboot`.
4. Boot from the External Drive and continue the setup.

The process was so straightforward that I tried to do everything from the Linux
side, but I encountered some issues and eventually gave up. It may actually be
doable, because the issues were small:

1. You need to compile the edge version of `ntfs-3g`, and build `wimlib` (linux
  alternative to dism) linking it against the edge version of `ntfs-3g` in order
  to expand Windows 10 images. [Source][2].

2. There isn't a tool like `bcdboot` for Linux, so you need to [install BOOTMGR
  manually][3].

In the end, I decided to do everything from WinPE and the most straightforward
way to use WinPE is to boot into the Windows Setup.

## The actual steps

1. Download the ISO from the [official website][4].

2. Boot into the Windows Setup and open the Command Prompt with `Shift + F10`.

    This step is intentionally left ambiguous. There are too many many ways to
    boot into the Windows Setup. You can [create a bootable USB][5], burn a DVD,
    you can also mount the ISO and your external disk in VirtualBox.

    This article will use the VirtualBox approach, you can check the
    instructions to mount your external disk [here][6].

3. Run `diskpart` to partition and format the disk.

    ```
    list disk                           // list every disk and their number
    select disk 0                       // change 0 with the # you wish to use
    clean
    create partition primary size=512
    format fs=fat32 quick label=BOOT
    active
    assign
    create partition primary
    format fs=ntfs quick label=Windows
    assign
    list volume                         // you'll need the drive letters later
    exit
    ```

    These steps will create an MBR layout in the disk and a boot partition, this
    is intentional to achieve compatibility with both firmwares: BIOS and UEFI.

    In this example, the `C` drive is the `BOOT` partition, the `D` drive is the
    Windows Setup DVD, and the `E` drive is the `Windows` partition. The drives
    in your PC will probably be different, so you'll need to update the
    instructions for your particular configuration.

4. You'll need the find the `index` of the edition of Windows you wish to
    install using `dism`. Remember to adjust the `/imagefile:` argument if
    required:

    ```
    dism /get-imageinfo /imagefile:D:\sources\install.wim
    ```

5. Proceed to expand the Windows image with `dism`, in this example I'll be
    installing `Windows 10 Pro`, which is the 6th index. Remember to adjust the
    `/imagefile:`, `/index:` and `/applydir:` arguments if required:

    ```
    dism /apply-image /imagefile:D:\sources\install.wim /index:6 /applydir:E:\
    ```

6. Install BOOTMGR to the external drive. Remember to adjust the arguments if
    required; In this example I'm telling `bcdboot` that Windows was expanded to
    `E:\Windows` and that it should install the bootloader in `C:`; the `/f ALL`
    argument installs both UEFI and BIOS bootloaders:

    ```
    bcdboot E:\Windows /s C: /f ALL
    ```

7. Hide the `BOOT` partition using `diskpart`.

    ```
    list volume
    select volume 1                     // select the `BOOT` volume
    set id=1c                           // `1c` is Hidden FAT32 (LBA)
    exit
    ```

8. Finally, turn off the VM, plug the external drive to your PC and continue the
    Windows Setup. It will proceed to install the drivers and apply the initial
    configuration.

[1]: https://en.wikipedia.org/wiki/Windows_To_Go
[2]: https://wimlib.net/forums/viewtopic.php?f=1&t=4
[3]: http://reboot.pro/topic/20468-create-a-windows-system-from-scratch-using-linux/
[4]: https://www.microsoft.com/en-us/software-download/windows10ISO
[5]: https://askubuntu.com/a/487970
[6]: https://www.serverwatch.com/server-tutorials/using-a-physical-hard-drive-with-a-virtualbox-vm.html