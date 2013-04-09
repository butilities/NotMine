#!/usr/bin/python

# Poison Ivy scanner from the malware.lu team.
# source: http://www.malware.lu/Pro/RAP002_APT1_Technical_backstage.1.0.pdf

def check_poison(self, host, port, res):

		try:
				af, socktype, proto, canonname, sa = res
				s = socket.socket(af, socktype, proto)
				s.settimeout(6)
				s.connect(sa)
				stage1 = "\x00" * 0x100
				s.sendall(stage1)
				data = s.recv(0x100)

				if len(data) != 0x100:
						s.close()
						return
				data = s.recv(0x4)
				s.close()
				
				if data != "\xD0\x15\x00\x00":
						return
				print "%s Poison %s %s:%d" % (datetime.datetime.now(), host, sa[0], sa[1])

		except socket.timeout as e:
				pass
		except socket.error as e:
				pass

