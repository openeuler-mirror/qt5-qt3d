Name:          qt5-qt3d
Version:       5.11.1
Release:       4 
Summary:       Qt5 - Qt3D C++ APIs and QML bindings
License:       LGPLv2 with exceptions or GPLv3 with exceptions
Url:           http://www.qt.io
Source0:       https://download.qt.io/new_archive/qt/5.11/%{version}/submodules/qt3d-everywhere-src-%{version}.tar.xz

BuildRequires: qt5-rpm-macros >= %{version} qt5-qtbase-private-devel qt5-qtdeclarative-devel
BuildRequires: qt5-qtimageformats qt5-qtxmlpatterns-devel pkgconfig(assimp) >= 3.3.1
Requires:      qt5-qtimageformats >= %{version}
%{?_qt5:Requires: %{_qt5} = %{_qt5_version}}

%description
Qt 3D support for 2D and 3D rendering in both Qt C++ and Qt Quick applications for
near-realtime simulation systems.

%package       devel
Summary:       Provides development files for qt5-qt3d
Requires:      qt5-qt3d = %{version}-%{release} qt5-qtbase-devel

Provides:      %{name}-examples = %{version}-%{release}
Obsoletes:     %{name}-examples < %{version}-%{release}

%description   devel
Provides development files and programming examples for qt5-qt3d.

%prep
%autosetup  -n qt3d-everywhere-src-%{version}

%build
%{qmake_qt5}
%make_build

%install
make install INSTALL_ROOT=%{buildroot}

pushd %{buildroot}%{_qt5_libdir}
for prl_file in libQt5*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
popd

%post
/sbin/ldconfig
%postun
/sbin/ldconfig

%files
%license LICENSE.GPL* LICENSE.LGPL*
%{_qt5_libdir}/{libQt53D*.so.5*}
%{_qt5_qmldir}/{Qt3D/,QtQuick/Scene3D/,QtQuick/Scene2D/}
%{_qt5_plugindir}/{sceneparsers/,renderplugins/,geometryloaders/}

%files devel
%{_qt5_bindir}/qgltf
%{_qt5_libdir}/{libQt53D*.so}
%{_qt5_libdir}/{libQt53D*.prl}
%{_qt5_libdir}/cmake/{Qt53DQuickScene2D,Qt53DQuickAnimation,Qt53DAnimation,Qt53DQuickExtras}
%{_qt5_libdir}/cmake/{Qt53DExtras,Qt53DQuickInput,Qt53DLogic,Qt53DRender/}
%{_qt5_libdir}/cmake/{Qt53DQuickRender/,Qt53DInput,Qt53DQuick,Qt53DCore/}
%{_qt5_includedir}/{Qt3DQuick,Qt3DQuickScene2D,Qt3DQuickAnimation,Qt3DAnimation}
%{_qt5_includedir}/{Qt3DQuickExtras,Qt3DExtras,Qt3DQuickInput/,Qt3DLogic/}
%{_qt5_includedir}/{Qt3DRender/,Qt3DQuickRender/,Qt3DCore/,Qt3DInput/}
%{_qt5_libdir}/pkgconfig/*.pc
%{_qt5_archdatadir}/mkspecs/modules/*.pri
%if 0%{?_qt5_examplesdir:1}
%{_qt5_examplesdir}/
%endif

%changelog
* Mon Sep 14 2020 liuweibo <liuweibo10@huawei.com> - 5.11.1-4
- Fix Source0

* Tue Dec 3 2019 Tianfei <tianfei16@huawei.com> - 5.11.1-3
- Package init

