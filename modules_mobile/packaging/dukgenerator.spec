Name:      dukgenerator
Summary:   nothing
Version:    1.0.0
Release:    7
Group:      security
License:    Apache License, Version 2.0
Source0:    %{name}-%{version}.tar.gz
BuildRequires: cmake

BuildRequires: pkgconfig(openssl)
BuildRequires: pkgconfig(cryptsvc)

%description

%package devel
Summary: nothing
Group: security
Requires: %{name} = %{version}-%{release}

%description devel

%prep
%setup -q

%build
MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
cmake . -DCMAKE_INSTALL_PREFIX=%{_prefix} -DFULLVER=%{version} -DMAJORVER=${MAJORVER} -DDESCRIPTION=%{summary}
make %{?jobs:-j%jobs}


%install
rm -rf %{buildroot}
#%make_install
%{__make} DESTDIR=%{?buildroot:%{buildroot}} INSTALL_ROOT=%{?buildroot:%{buildroot}} install
rm -f %{?buildroot:%{buildroot}}%{_infodir}/dir
find %{?buildroot:%{buildroot}} -regex ".*\\.la$" | xargs rm -f --

mkdir -p %{buildroot}/usr/share/license
cp LICENSE.APLv2 %{buildroot}/usr/share/license/%{name}


%files
%{_libdir}/*.a
%{_datadir}/license/%{name}


%files devel
%{_includedir}/*
%{_libdir}/pkgconfig/dukgenerator.pc
