
<div align="center">  
    <a href="https://github.com/ccccchhhheeenng/Python-GUI--Setup-Windows-Server-with-python/stargazers"><img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/ccccchhhheeenng/Python-GUI--Setup-Windows-Server-with-python"></a>
    <a href="https://twitter.com/ccccchhhheeenng"><img alt="Twitter Follow" src="https://img.shields.io/twitter/follow/ccccchhhheeenng"></a>

</div>

> [!WARNING]  
> This app can only run on Windows Server.

# Windows Server Tool


- [Download latest](https://github.com/ccccchhhheeenng/Windows-Server-Tool/raw/refs/heads/main/Application.exe)

<div align="center">
  <a href="https://github.com/ccccchhhheeenng/Python-GUI--Setup-Windows-Server-with-python/stargazers">
    <img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/ccccchhhheeenng/Python-GUI--Setup-Windows-Server-with-python">
  </a>
  <a href="https://twitter.com/ccccchhhheeenng">
    <img alt="Twitter Follow" src="https://img.shields.io/twitter/follow/ccccchhhheeenng">
  </a>
</div>

# Setup-Windows-Server-with-python

## Releases
### v1.0.0
Released at 2024/04/05

- [Windows Executable Download](https://github.com/ccccchhhheeenng/Python-GUI--Setup-Windows-Server-with-python/raw/main/Application.exe)
- [Source Code](https://github.com/ccccchhhheeenng/Python-GUI--Setup-Windows-Server-with-python/raw/main/main.py)

## How to use
> [!WARNING]
> This app can only run on Windows Server.

### Installation steps
1. Download the latest release.
2. Open it and enjoy the app.

### DHCP
> [!IMPORTANT]
> Please install the DHCP feature before setup.

Input the config and press **Finish** to setup.

<details>
<summary>Example</summary>

```text
StartRange:  192.168.0.100
EndRange:    192.168.0.200
SubnetMask:  255.255.255.0
ScopeName:   DHCP_Scope
DNS Address: 1.1.1.1
Router IP:   192.168.0.1
```

</details>

![DHCP Setup Screenshot](https://hackmd.io/_uploads/B1uzlprM0.png)

### DNS
> [!IMPORTANT]
> Please install the DNS feature before setup.

#### Forward lookup

<details>
<summary>Add Primary Zone</summary>

This function can add a DNS zone.

Example:

```text
Zone Name: hello.world
```

![Add Primary Zone Screenshot](https://hackmd.io/_uploads/SyY5MTHfA.png)

</details>

<details>
<summary>Add DNS Record</summary>

This function can add a DNS record.

Supported record types: `A`, `AAAA`, `CNAME`

Steps:

1. Enter the zone where you want to add a DNS record.

![Set Zone Screenshot](https://hackmd.io/_uploads/Sk4drTBzR.png)

2. Enter the record name and IP address.

![Set Record Screenshot](https://hackmd.io/_uploads/B14cSpHzC.png)

Example:

```text
1.
Set Zone:    hello.world
Record Type: A

2.
Name:        aaa
IP Address:  127.0.0.1
```

</details>

<details>
<summary>Remove Primary Zone</summary>

(TODO)

</details>

<details>
<summary>Remove DNS Record</summary>

(TODO)

</details>

#### Reverse lookup

#### Set Forwarder


