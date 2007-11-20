Summary:	Open Source implementation of IEEE 802.1AB
Name:		openlldp
%define		_rc	alpha
%define		rel	0.1
Version:	0.3
Release:	0.%{_rc}.%{rel}
License:	GPL
Group:		Networking
Source0:	http://dl.sourceforge.net/openlldp/%{name}-%{version}%{_rc}.tar.gz
# Source0-md5:	131abc8c2563d33c4537d1c6dcb5c121
URL:		http://openlldp.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The OpenLLDP project aims to provide a comprehensive implementation of the
IEEE standard 802.1AB Link Layer Discovery Protocol. LLDP is an industry
standard protocol designed to supplant proprietary Link-Layer protocols such
as Extreme's EDP (Extreme Discovery Protocol) and CDP (Cisco Discovery
Protocol). The goal of LLDP is to provide an inter-vendor compatible
mechanism to deliver Link-Layer notifications to adjacent network devices.
The Open Source implementation of LLDP provided by the OpenLLDP project is
intended to help foster wider adoption of LLDP.

%prep
%setup -q -n %{name}-%{version}%{_rc}

%build
%{__aclocal}
%{__autoconf}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog LICENSE README
%attr(755,root,root) %{_sbindir}/lldpd
