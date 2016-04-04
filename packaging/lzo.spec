Name:           lzo
Version:        2.08
Release:        0
License:        GPL-2.0+
Summary:        Data compression library with very fast (de)compression
Url:            http://www.oberhumer.com/opensource/lzo/
Group:          System/Libraries
Source0:        http://www.oberhumer.com/opensource/lzo/download/%{name}-%{version}.tar.gz
Source1001:     lzo.manifest
BuildRequires:  zlib-devel
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
LZO is a portable lossless data compression library written in ANSI C.
It offers pretty fast compression and very fast decompression.
Decompression requires no memory. In addition there are slower
compression levels achieving a quite competitive compression ratio
while still decompressing at this very high speed.

%package minilzo
Summary:        Mini version of lzo for apps which don't need the full version
Group:          System/Libraries
Requires:       %{name} = %{version}
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description minilzo
A small (mini) version of lzo for embedding into applications which don't need
full blown lzo compression support.

%package devel
Summary:        Development files for the lzo library
Group:          Development/Libraries
Requires:       %{name} = %{version}
Requires:       zlib-devel

%description devel
LZO is a portable lossless data compression library written in ANSI C.
It offers pretty fast compression and very fast decompression.
This package contains development files needed for lzo.

%prep
%setup -q
cp %{SOURCE1001} .


%build
export CFLAGS+=" -fvisibility=hidden"
  export CXXFLAGS+=" -fvisibility=hidden"
  

%configure --disable-static \
    --disable-dependency-tracking \
    --enable-shared \
    CFLAGS="`echo $CFLAGS | sed 's/-O2//g'`"

%__make %{?_smp_mflags}

# build minilzo too (bz 439979)
gcc %{optflags} -O2 -g -fpic -Iinclude/lzo -o minilzo/minilzo.o -c minilzo/minilzo.c
gcc -g -shared -o libminilzo.so.0 -Wl,-soname,libminilzo.so.0 minilzo/minilzo.o
%install
%make_install

install -m 755 libminilzo.so.0 %{buildroot}%{_libdir}
ln -sf libminilzo.so.0 %{buildroot}%{_libdir}/libminilzo.so
install -p -m 644 minilzo/minilzo.h %{buildroot}%{_includedir}/lzo
rm -f %{buildroot}%{_datadir}/doc/%{name}/COPYING


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%post minilzo -p /sbin/ldconfig

%postun minilzo -p /sbin/ldconfig


%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license COPYING
%{_libdir}/liblzo2.so.*

%files minilzo
%manifest %{name}.manifest
%defattr(-,root,root,-)
%doc minilzo/README.LZO
%{_libdir}/libminilzo.so.0

%files devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
%doc %{_datadir}/doc/%{name}/AUTHORS
%doc %{_datadir}/doc/%{name}/LZO*
%doc %{_datadir}/doc/%{name}/NEWS
%doc %{_datadir}/doc/%{name}/THANKS
%{_includedir}/lzo
%{_libdir}/lib*lzo*.so
