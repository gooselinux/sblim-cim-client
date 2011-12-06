%define provider_dir %{_libdir}/cmpi
%define tog_pegasus_version 2:2.5.1

# sblim-cim-client macros
%define archive_folder_name cim-client
%define cim_client_jar_file sblimCIMClient
%define slp_name sblim-slp-client
%define slp_client_jar_file sblimSLPClient

# there's no reason to produce debuginfo package
#%global debug_package %{nil}

Summary:        Java CIM Client library
Name:           sblim-cim-client
Version:        1.3.9.1
Release:        1%{?dist}
License:        EPL
Group:          Development/Libraries
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
URL:            http://sourceforge.net/projects/sblim/
Source0:        http://downloads.sourceforge.net/project/sblim/%{name}/%{version}/%{name}-%{version}-src.zip
Source1:        http://downloads.sourceforge.net/project/sblim/%{name}/%{version}/%{name}-samples-%{version}-src.zip

BuildArch:      noarch

BuildRequires:  java-devel >= 1.4
BuildRequires:  jpackage-utils >= 0:1.5.32
BuildRequires:  xerces-j2 >= 2.7.1
BuildRequires:  ant >= 0:1.6
BuildRequires:  dos2unix

Requires:       java >= 1.4
Requires:       jpackage-utils >= 0:1.5.32
Requires:       xerces-j2 >= 2.7.1
Requires:       tog-pegasus >= %{tog_pegasus_version}

%description
The purpose of this package is to provide a CIM Client Class Library for Java
applications. It complies to the DMTF standard CIM Operations over HTTP and
intends to be compatible with JCP JSR48 once it becomes available. To learn
more about DMTF visit http://www.dmtf.org.
More infos about the Java Community Process and JSR48 can be found at
http://www.jcp.org and http://www.jcp.org/en/jsr/detail?id=48.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Documentation
Requires:       sblim-cim-client = %{version}-%{release}

%description javadoc
Javadoc for sblim-cim-client.

%package manual
Summary:        Manual and sample code for %{name}
Group:          Documentation
Requires:       sblim-cim-client = %{version}-%{release}

%description manual
Manual and sample code for sblim-cim-client.

%prep
%setup -q -n %{archive_folder_name}
rm version.txt
%setup -q -T -D -b 1 -n %{archive_folder_name}

%build
export ANT_OPTS="-Xmx256m"
ant \
        -Dbuild.compiler=modern \
        -DManifest.version=%{version} \
        build-release

%install
rm -rf $RPM_BUILD_ROOT
# documentation
dos2unix COPYING README ChangeLog NEWS
mkdir -p $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
install COPYING $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
install README $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
install ChangeLog $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
install NEWS $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
# samples (also into _docdir)
pushd samples
  dos2unix README.samples
  pushd org/sblim/slp/example
    dos2unix *
  popd
  pushd org/sblim/wbem/cimclient/sample
    dos2unix *
  popd
popd
install samples/README.samples $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
cp -pr  samples/org $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
# default cim.defaults
dos2unix cim.defaults slp.conf
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/java
install cim.defaults $RPM_BUILD_ROOT%{_sysconfdir}/java/%{name}.properties
install slp.conf $RPM_BUILD_ROOT%{_sysconfdir}/java/%{slp_name}.properties
# jar
mkdir -p $RPM_BUILD_ROOT%{_javadir}
install %{archive_folder_name}/%{cim_client_jar_file}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
(
  cd $RPM_BUILD_ROOT%{_javadir} &&
    ln -sf %{name}-%{version}.jar %{cim_client_jar_file}.jar;
    ln -sf %{name}-%{version}.jar %{name}.jar;
)
install %{archive_folder_name}/%{slp_client_jar_file}.jar $RPM_BUILD_ROOT%{_javadir}/%{slp_name}-%{version}.jar
(
  cd $RPM_BUILD_ROOT%{_javadir} &&
    ln -sf %{slp_name}-%{version}.jar %{slp_client_jar_file}.jar;
    ln -sf %{slp_name}-%{version}.jar %{slp_name}.jar;
)
# javadoc
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
#cp -pr %{archive_folder_name}/doc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
#cp -pr doc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}

%files
%defattr(0644,root,root,0755)
%config(noreplace) %{_sysconfdir}/java/%{name}.properties
%config(noreplace) %{_sysconfdir}/java/%{slp_name}.properties
%dir %{_datadir}/doc/%{name}-%{version}
%doc %{_docdir}/%{name}-%{version}/COPYING
%doc %{_docdir}/%{name}-%{version}/README
%doc %{_docdir}/%{name}-%{version}/ChangeLog
%doc %{_docdir}/%{name}-%{version}/NEWS
%{_javadir}/%{name}.jar
%{_javadir}/%{name}-%{version}.jar
%{_javadir}/%{cim_client_jar_file}.jar
%{_javadir}/%{slp_name}.jar
%{_javadir}/%{slp_name}-%{version}.jar
%{_javadir}/%{slp_client_jar_file}.jar

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}

%files manual
%defattr(0644,root,root,0755)
%doc %{_docdir}/%{name}-%{version}/README.samples
%doc %{_docdir}/%{name}-%{version}/COPYING
%doc %{_docdir}/%{name}-%{version}/org

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Mon Oct  5 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.3.9.1-1
- Initial support
