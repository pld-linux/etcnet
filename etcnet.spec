# TODO
# - pld dependencies
# - pld files
# - ...!
# - relocate static scripts in /etc/net to /lib/etcnet or patch etckeeper to ignore the files to fix etckeeper tracking etcnet code
Summary:	/etc/net network configuration system
Name:		etcnet
Version:	0.9.10
Release:	0.1
License:	GPL v2
Group:		Base
# Extracted from ftp://ftp.altlinux.org/pub/distributions/ALTLinux/Sisyphus/files/SRPMS/etcnet-0.9.10-alt10.src.rpm
Source0:	%{name}-%{version}.tar
# Source0-md5:	04463f3999893bd4265993392c0772b0
Requires:	/sbin/chkconfig
Requires:	etcnet-defaults = %{version}-%{release}
Requires:	grep
Requires:	ifrename >= 28-alt5.pre10
Requires:	iproute2
Requires:	sed
Requires:	service
Requires:	setup >= 0:2.1.9-ipl18mdk
Requires:	startup >= 0:0.9.3-alt1
Provides:	network-config-subsystem
Conflicts:	ethtool < 0:3-alt4
Conflicts:	ifplugd < 0.28-alt2
Conflicts:	ipset < 4.1-alt2
Conflicts:	net-scripts
Conflicts:	systemd < 1:210-alt7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
/etc/net represents a new approach to Linux network configuration
tasks.

Inspired by the limitations of traditional network configuration
subsystems, /etc/net provides builtin support for configuration
profiles, interface name management, removable devices, full iproute2
command set, interface dependencies resolution, QoS and firewall
configuration frameworks. /etc/net provides support for the following
interface types: Ethernet, WiFi (WEP), IPv4/IPv6 tunnels, PSK IPSec
tunnels, VLAN, PLIP, Ethernet bonding and bridging, traffic equalizer,
Pent@NET, Pent@VALUE, SkyStar-2, TUN/TAP, OpenVPN TUN/TAP, OpenSSH
TUN/TAP, usbnet and PPP. Due to its modular structure, support for new
interface types can be added without overall design changes.

%package full
Summary:	/etc/net plus everything it can work with
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}
Requires:	avahi-autoipd
Requires:	bridge-utils
Requires:	dhcpcd >= 1.3.22pl4-alt3
Requires:	ebtables
Requires:	ethtool >= 0:3-alt4
Requires:	hotplug
Requires:	ifplugd >= 0.28-alt2
Requires:	ipset >= 4.1-alt2
Requires:	iptables
Requires:	iptables
Requires:	ncpfs
Requires:	openvpn
Requires:	ppp
Requires:	pptp-client
Requires:	rp-pppoe-base >= 3.6-alt2
Requires:	tunctl
Requires:	vlan-utils
Requires:	wireless-tools
Requires:	wpa_supplicant

%description full
This virtual package requires /etc/net and all packages that may
appear useful for /etc/net.

Accurate requirements should result in correct package versions in PLD
Linux system.

%package defaults-desktop
Summary:	/etc/net defaults for a Linux desktop
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}
Provides:	%{name}-defaults = %{version}-%{release}
Conflicts:	%{name}-defaults-server

%description defaults-desktop
This package contains default options for a Linux desktop.

%package defaults-server
Summary:	/etc/net defaults for a Linux server
Group:		Applications/Networking
Requires:	%{name} = %{version}-%{release}
Provides:	%{name}-defaults = %{version}-%{release}
Conflicts:	%{name}-defaults-desktop

%description defaults-server
This package contains default options for a Linux server.

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT
# Common part first, distribution-specific files later.
%{__make} -f contrib/Makefile install \
	prefix=$RPM_BUILD_ROOT

cp -p contrib/50-ALTLinux-desktop $RPM_BUILD_ROOT%{_sysconfdir}/net/options.d
cp -p contrib/50-ALTLinux-server $RPM_BUILD_ROOT%{_sysconfdir}/net/options.d

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ $1 -eq 1 ]; then
	# This is a fresh install.
	/sbin/chkconfig --add network
fi

%preun
if [ $1 -eq 0 ]; then
	# This is an erase.
	/sbin/chkconfig --del network
fi

# since 0.5.0 we have 'network' chkconfig entry instead of 'etcnet' one
%triggerun -- %{name} < 0.5.1
if [ $2 -gt 0 ]; then
	# This is etcnet upgrade.
	/sbin/chkconfig --del etcnet
	/sbin/chkconfig --add network
fi

%triggerpostun -- net-scripts
/sbin/chkconfig --add network

# We used to ship some Ruby contrib scripts, but having Ruby installed
# by dependency isn't an idea most normal users would like. So let
# people adjust their environment manually for particular contribs to work.
#%%add_findreq_skiplist /etc/net/scripts/contrib/*

%files
%defattr(644,root,root,755)
%doc docs/README* docs/ChangeLog docs/TODO docs/wiki-RU/
%doc examples/ contrib/
%dir %{_sysconfdir}/net
%dir %{_sysconfdir}/net/scripts
%dir %{_sysconfdir}/net/ifaces
%dir %{_sysconfdir}/net/ifaces/default
%dir %{_sysconfdir}/net/ifaces/lo
%dir %{_sysconfdir}/net/ifaces/unknown
%dir %{_sysconfdir}/net/options.d
%{_sysconfdir}/net/scripts/*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/net/ifaces/default/*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/net/ifaces/unknown/*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/net/ifaces/lo/*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/net/sysctl.conf
%attr(754,root,root) /etc/rc.d/init.d/network
%{systemdunitdir}/*
%exclude %{_sysconfdir}/net/options.d/50-*
%config %{_sysconfdir}/net/options.d/*
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/network
%{_mandir}/man5/*
%{_mandir}/man8/*
/sbin/ifup
/sbin/ifdown
/sbin/eqos
/sbin/efw

%files defaults-desktop
%defattr(644,root,root,755)
%config %{_sysconfdir}/net/options.d/50-ALTLinux-desktop

%files defaults-server
%defattr(644,root,root,755)
%config %{_sysconfdir}/net/options.d/50-ALTLinux-server

%files full
%defattr(644,root,root,755)
