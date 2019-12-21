# EcoNav ♻️

_Warning: Project is in early development_

**[Read the design doc for more information](./docs/design_doc.pdf)**

## What is EcoNav?

EcoNav is a system you install in your car that analyzes your driving habits and give you feedback in real time and after your trip on how to improve your fuel efficency.

## Required hardware

- Raspberry Pi
- ELM327 ODBII port scanner
- Raspberry Pi Camera Module
- Android smartphone with Android 9 +

## Debugging

### Raspberry Pi

To SSH into the raspberry pi when connected via ethernet cable

- Go into your network settings and change the IPv4 mode to `Shared to other computer`
- The hostname will be `hostname.local` (i.e `econav.local`)
