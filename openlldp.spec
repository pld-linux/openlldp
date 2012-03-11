%define		subver	alpha
%define		rel	0.3
Summary:	Open Source implementation of IEEE 802.1AB
Summary(pl.UTF-8):	Implementacja IEEE 802.1AB z otwartymi źródłami
Name:		openlldp
Version:	0.4
Release:	0.%{subver}.%{rel}
License:	GPL
Group:		Networking
Source0:	http://dl.sourceforge.net/openlldp/%{name}-%{version}%{subver}.tar.bz2
# Source0-md5:	68d11173cfaecd5ae00ec57a28d94ee5
Source1:	%{name}-lldp.8
Source2:	%{name}-lldp.init
Source3:	%{name}-lldp.sysconfig
Source4:	%{name}-lldp.service
Patch0:		%{name}-noproc.patch
Patch1:		%{name}-bpf.patch
URL:		http://openlldp.sourceforge.net/
BuildRequires:	autoconf >= 1.5
BuildRequires:	automake
BuildRequires:	libconfuse-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The OpenLLDP project aims to provide a comprehensive implementation of
the IEEE standard 802.1AB Link Layer Discovery Protocol. LLDP is an
industry standard protocol designed to supplant proprietary Link-Layer
protocols such as Extreme's EDP (Extreme Discovery Protocol) and CDP
(Cisco Discovery Protocol). The goal of LLDP is to provide an
inter-vendor compatible mechanism to deliver Link-Layer notifications
to adjacent network devices. The Open Source implementation of LLDP
provided by the OpenLLDP project is intended to help foster wider
adoption of LLDP.

%description -l pl.UTF-8
Celem projektu OpenLLDP jest dostarczenie kompletnej implementacji
standardu IEEE 802.1AB Link Layer Discovery Protocol (protokołu
wykrywania w warstwie połączenia). LLDP to standardowy protokół
zaprojektowany w celu wyparcia własnościowych protokołów warstwy
połączenia, takich jak EDP (Extreme Discovery Protocol) czy CDP (Cisco
Discovery Protocol). Celem LLDP jest udostępnienie mechanizmu
kompatybilnego między producentami dostarczającymi powiadomienia w
warstwie połączenia o sąsiednich urządzeniach sieciowych.
Implementacja z otwartymi źródłami udostępniana przez projekt OpenLLDP
ma wspomóc szersze adoptowanie LLDP.

%prep
%setup -q -n %{name}-%{version}%{subver}
%patch0 -p1
%patch1 -p1

%build
%{__aclocal}
%{__autoconf}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{sysconfig,rc.d/init.d},%{_mandir}/man8,%{systemdunitdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{_mandir}/man8/lldp.8
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/lldpd
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/lldpd
install %{SOURCE4} $RPM_BUILD_ROOT%{systemdunitdir}/lldpd.service

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add lldpd
%service lldpd restart "OpenLLDP Daemon"
%systemd_post lldpd.service

%preun
if [ "$1" = "0" ]; then
        %service lldpd stop
        /sbin/chkconfig --del lldpd
fi
%systemd_preun lldpd.service

%postun
%systemd_reload

%triggerpostun -- openlldp < 0.4
%systemd_trigger lldpd.service

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog LICENSE README
%attr(754,root,root) /etc/rc.d/init.d/lldpd
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/lldpd
%{systemdunitdir}/lldpd.service
%attr(755,root,root) %{_sbindir}/lldpd
%attr(755,root,root) %{_bindir}/lldpneighbors
%{_mandir}/man8/*.8*
