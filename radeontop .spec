%global major 0
%define libname %mklibname XXX %{major}
%define devname %mklibname -d XXX
%global commit ef27e8b8ff189cfef409f2fb503ccfe445bcb1ec
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global checkout .20200415git%{shortcommit}
%global debug_package %{nil}

Summary:	View GPU utilization of AMD/ATI Radeon devices
Name:		radeontop
Group:		System/Kernel and hardware
Version:	1.3
Release:	%mkrel 1
License:	GPLv3
URL:		https://github.com/clbr/%{name}

# wget https://github.com/clbr/radeontop/archive/v1.0/radeontop-1.0.tar.gz
#Source0:    %{url}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
Source0:	https://github.com/clbr/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:	%{name}.metainfo.xml

BuildRequires:	asciidoc gettext
BuildRequires:	appstream-util
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	pkgconfig(pciaccess)
BuildRequires:	pkgconfig(libdrm)
BuildRequires:	pkgconfig(xcb)


%description
RadeonTop shows the utilization of your GPU, both in general and by blocks.
Supported cards are R600 and up.

%prep
%autosetup -n %{name}-%{version}

%build
# configure doesn't exist, but we need the exported CFLAGS and friends
%configure || :

%make_build PREFIX=%{_prefix} amdgpu=1 xcb=1 CC="gcc -g"

%install
%make_install PREFIX=%{_prefix} LIBDIR=%{_lib}   
%find_lang %{name}

# Add AppStream metadata
install -Dm 0644 -p %{SOURCE1} \
	%{buildroot}%{_datadir}/metainfo/%{name}.metainfo.xml

%check
# Validate Appstream metadata
appstream-util validate-relax --nonet %{buildroot}/%{_datadir}/metainfo/%{name}.metainfo.xml

%files -f %{name}.lang
%doc README.md 
%license COPYING
%{_sbindir}/%{name}
# Workaround failure to build on /usr/lib64
%{_libdir}/lib%{name}_xcb.so
%{_mandir}/man1/%{name}.1*
#AppStream metadata
%{_metainfodir}/%{name}.metainfo.xml

