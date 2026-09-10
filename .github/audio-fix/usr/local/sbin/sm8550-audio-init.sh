#!/bin/bash
# SM8550 (Xiaomi Pad 6S Pro) audio bring-up: register sound card after boot.
set -e
sleep 3

modprobe soundwire-qcom
modprobe snd-soc-wcd-common
modprobe snd-soc-wcd-mbhc
modprobe snd-soc-wcd-classh
modprobe snd-soc-wcd938x-sdw
modprobe snd-soc-wcd938x
modprobe snd-soc-lpass-macro-common
modprobe snd-soc-lpass-rx-macro
modprobe snd-soc-lpass-tx-macro
modprobe snd-soc-lpass-va-macro
modprobe snd-soc-lpass-wsa-macro

# Re-trigger the machine driver so it binds to the codecs now present.
modprobe -r snd-soc-sc8280xp 2>/dev/null || true
modprobe snd-soc-sc8280xp

if [ -d /proc/asound/card0 ]; then
	logger -t sm8550-audio 'sound card registered OK'
else
	logger -t sm8550-audio 'sound card FAILED to register'
fi