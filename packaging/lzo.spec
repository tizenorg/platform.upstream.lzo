
Name:       lzo
Summary:    Data compression library with very fast (de)compression
Version:    2.03
Release:    3.15
Group:      System/Libraries
License:    GPLv2+
URL:        http://www.oberhumer.com/opensource/lzo/
Source0:    http://www.oberhumer.com/opensource/lzo/download/%{name}-%{version}.tar.gz
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires:  zlib-devel


%description
LZO is a portable lossless data compression library written in ANSI C.
It offers pretty fast compression and very fast decompression.
Decompression requires no memory. In addition there are slower
compression levels achieving a quite competitive compression ratio
while still decompressing at this very high speed.



%package minilzo
Summary:    Mini version of lzo for apps which don't need the full version
Group:      System/Libraries
Requires:   %{name} = %{version}-%{release}
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description minilzo
A small (mini) version of lzo for embedding into applications which don't need
full blown lzo compression support.


%package devel
Summary:    Development files for the lzo library
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
Requires:   zlib-devel

%description devel
LZO is a portable lossless data compression library written in ANSI C.
It offers pretty fast compression and very fast decompression.
This package contains development files needed for lzo.



%prep
%setup -q -n %{name}-%{version}


%build

%configure --disable-static \
    --disable-dependency-tracking \
    --enable-shared \
    CFLAGS="`echo $CFLAGS | sed 's/-O2//g'`"

make %{?jobs:-j%jobs}

# build minilzo too (bz 439979)
gcc %{optflags} -O2 -g -fpic -Iinclude/lzo -o minilzo/minilzo.o -c minilzo/minilzo.c
#gcc -O2 -g -fpic -Iinclude/lzo -o minilzo/minilzo.o -c minilzo/minilzo.c
gcc -g -shared -o libminilzo.so.0 -Wl,-soname,libminilzo.so.0 minilzo/minilzo.o
%install
rm -rf %{buildroot}
%make_install 

install -m 755 libminilzo.so.0 $RPM_BUILD_ROOT%{_libdir}
ln -s libminilzo.so.0 $RPM_BUILD_ROOT%{_libdir}/libminilzo.so
install -p -m 644 minilzo/minilzo.h $RPM_BUILD_ROOT%{_includedir}/lzo



%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig



%post minilzo -p /sbin/ldconfig

%postun minilzo -p /sbin/ldconfig




%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING THANKS NEWS
%{_libdir}/liblzo2.so.*


%files minilzo
%defattr(-,root,root,-)
%doc minilzo/README.LZO
%{_libdir}/libminilzo.so.0

%files devel
%defattr(-,root,root,-)
%doc doc/LZOAPI.TXT doc/LZO.FAQ doc/LZO.TXT
%{_includedir}/lzo
%{_libdir}/lib*lzo*.so

