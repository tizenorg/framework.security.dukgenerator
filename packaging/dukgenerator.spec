Name:      dukgenerator
Summary:   nothing
Version:    1.0.1
Release:    7
Group:      security
License:    Apache License, Version 2.0
Source0:    %{name}-%{version}.tar.gz

%if "%{_repository}" == "wearable"

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
echo "########################################"
echo "TIZEN_PROFILE_WEARABLE"
echo "########################################"
cp -R modules_wearable/* .

%if 0%{?tizen_build_binary_release_type_eng}
export CFLAGS="$CFLAGS -DTIZEN_ENGINEER_MODE"
export CXXFLAGS="$CXXFLAGS -DTIZEN_ENGINEER_MODE"
export FFLAGS="$FFLAGS -DTIZEN_ENGINEER_MODE"
%endif
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


%else

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
echo "########################################"
echo "TIZEN_PROFILE_MOBILE"
echo "########################################"
cp -R modules_mobile/* .

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


%endif
