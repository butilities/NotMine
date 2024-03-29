#!/bin/sh

target="192.168.0.254"
conf="/etc/dnsmasq.conf"

src="http://pgl.yoyo.org/adservers/serverlist.php?hostformat=nohtml&showintro=0&mimetype=plaintext"

inc="/etc/dnsmasq.conf.inc"
out=/tmp/addblock-$(date +%s)
cp $conf $out
curl $src | awk '{print "address=/"$0"/'$target'"}' >> $out
[ -e $inc ] && (cat $inc >> !$)
sudo -u root uniq $out $conf
sudo rc.d restart dnsmaq
