%define		subver	alpha
%define		rel	1
Summary:	Open Source implementation of IEEE 802.1AB
Name:		openlldp
Version:	0.3
Release:	0.%{subver}.%{rel}
License:	GPL
Group:		Networking
Source0:	http://dl.sourceforge.net/openlldp/%{name}-%{version}%{subver}.tar.gz
# Source0-md5:	131abc8c2563d33c4537d1c6dcb5c121
Source1:	%{name}-lldp.8
Patch0:		%{name}-noproc.patch
Patch1:		%{name}-bpf.patch
Patch2:		%{name}-lldp_main.patch
Patch3:		%{name}-min_interfaces.patch
URL:		http://openlldp.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
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

%prep
%setup -q -n %{name}-%{version}%{subver}
%patch0 -p1
%patch1 -p1
%patch2 -p0
%patch3 -p0

%build
%{__aclocal}
%{__autoconf}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_mandir}/man8

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cp -a %{SOURCE1} $RPM_BUILD_ROOT%{_mandir}/man8/lldp.8

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog LICENSE README
%attr(755,root,root) %{_sbindir}/lldpd
%{_mandir}/man8/*.8*
