%{?scl:%scl_package jackson}
%{!?scl:%global pkg_name %{name}}

Name:		%{?scl_prefix}jackson
Version:	1.9.11
Release:	10%{?dist}
Summary:	Jackson Java JSON-processor
License:	ASL 2.0 or LGPLv2
URL:		http://jackson.codehaus.org
Source0:	http://jackson.codehaus.org/%{version}/%{pkg_name}-src-%{version}.tar.gz
# Build plain jar files instead of OSGi bundles in order to avoid depending on BND:
Patch0:		%{pkg_name}-build-plain-jars-instead-of-osgi-bundles.patch
# Don't require a repackaged version of ASM:
Patch1:		%{pkg_name}-dont-require-repackaged-asm.patch
# Don't bundle the ASM classes:
Patch2:		%{pkg_name}-dont-bundle-asm.patch
# fix for JACKSON-875
Patch3:		%{pkg_name}-1.9.11-to-1.9.13.patch
# Fix javadoc build
Patch4:		%{pkg_name}-%{version}-javadoc.patch

BuildArch:	noarch

Requires:	%{?scl_prefix_maven}joda-time %{!?scl:>= 1.6.2}
Requires:	%{?scl_prefix_maven}stax2-api %{!?scl:>= 3.1.1}
Requires:	%{?scl_prefix}jsr-311 %{!?scl:>= 1.1.1}
Requires:	%{?scl_prefix}objectweb-asm%{!?scl:3 >= 3.3}

BuildRequires:	%{?scl_prefix_java_common}ant %{!?scl:>= 1.8.2}
BuildRequires:	%{?scl_prefix_maven}javapackages-local
BuildRequires:	%{?scl_prefix_maven}joda-time %{!?scl:>= 1.6.2}
BuildRequires:	%{?scl_prefix_maven}stax2-api %{!?scl:>= 3.1.1}
BuildRequires:	%{?scl_prefix_maven}cglib %{!?scl:>= 2.2}
BuildRequires:	%{?scl_prefix_maven}groovy%{!?scl:18 >= 1.8.5}
BuildRequires:	%{?scl_prefix}jsr-311 %{!?scl:>= 1.1.1}
BuildRequires:	%{?scl_prefix}objectweb-asm%{!?scl:3 >= 3.3}
%{?scl:Requires: %scl_runtime}

%description
JSON processor (JSON parser + JSON generator) written in Java. Beyond basic
JSON reading/writing (parsing, generating), it also offers full node-based Tree
Model, as well as full OJM (Object/Json Mapper) data binding functionality.

%package javadoc
Summary:	Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n %{pkg_name}-src-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p0

# Remove all the binary jar files, as the packaging policies
# forbids using them:
find -name "*.jar" -delete

# Remove some tests to avoid additional dependencies:
rm src/test/org/codehaus/jackson/map/interop/TestHibernate.java
rm src/perf/perf/TestJsonPerf.java
rm src/test/org/codehaus/jackson/map/interop/TestGoogleCollections.java

%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
# Make symbolic links to the jar files expected by the ant build
# scripts:
ln -s $(build-classpath joda-time) lib/ext/joda-time.jar
ln -s $(build-classpath stax2-api) lib/xml/sta2-api.jar
ln -s $(build-classpath jsr-311) lib/jaxrs/jsr-311.jar
ln -s $(build-classpath objectweb-asm/asm) lib/ext/asm/asm.jar
ln -s $(build-classpath objectweb-asm/asm) lib/repackaged/jackson-asm.jar
ln -s $(build-classpath cglib/cglib) lib/ext/cglib/cglib-nodep.jar
ln -s $(build-classpath groovy/groovy) lib/ext/groovy/groovy.jar
ln -s $(build-classpath junit) lib/junit/junit.jar

sed -i "s,59 Temple Place,51 Franklin Street,;s,Suite 330,Fifth Floor,;s,02111-1307,02110-1301," \
 release-notes/lgpl/LGPL2.1

native2ascii -encoding UTF8 src/test/org/codehaus/jackson/jaxrs/TestUntouchables.java \
 src/test/org/codehaus/jackson/jaxrs/TestUntouchables.java

%{?scl:EOF}

%build
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
ant dist

%mvn_artifact dist/%{pkg_name}-core-asl-%{version}.pom dist/%{pkg_name}-core-asl-%{version}.jar
%mvn_artifact dist/%{pkg_name}-mapper-asl-%{version}.pom dist/%{pkg_name}-mapper-asl-%{version}.jar
%mvn_artifact dist/%{pkg_name}-xc-%{version}.pom dist/%{pkg_name}-xc-%{version}.jar
%mvn_artifact dist/%{pkg_name}-smile-%{version}.pom dist/%{pkg_name}-smile-%{version}.jar
%mvn_artifact dist/%{pkg_name}-mrbean-%{version}.pom dist/%{pkg_name}-mrbean-%{version}.jar
%mvn_artifact dist/%{pkg_name}-jaxrs-%{version}.pom dist/%{pkg_name}-jaxrs-%{version}.jar
%{?scl:EOF}

%install
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%mvn_install -J dist/javadoc
%{?scl:EOF}

%files -f .mfiles
%doc README.txt release-notes

%files javadoc -f .mfiles-javadoc
%doc README.txt release-notes

%changelog
* Wed Nov 23 2016 Tomas Repik <trepik@redhat.com> - 1.9.11-10
- scl conversion

* Fri Jul 08 2016 gil cattaneo <puntogil@libero.it> - 1.9.11-9
- rebuilt with new cglib

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.11-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Jan 30 2016 gil cattaneo <puntogil@libero.it> - 1.9.11-7
- rebuilt

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Feb 13 2015 gil cattaneo <puntogil@libero.it> 1.9.11-5
- built with groovy18

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Nov 14 2013 gil cattaneo <puntogil@libero.it> 1.9.11-3
- switch to java-headless (build)requires (rhbz#1068160)

* Thu Nov 14 2013 gil cattaneo <puntogil@libero.it> 1.9.11-2
- use objectweb-asm3

* Wed Sep 25 2013 gil cattaneo <puntogil@libero.it> 1.9.11-1
- Update to upstream version 1.9.11

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jul 24 2012 Juan Hernandez <juan.hernandez@redhat.com> - 1.9.4-5
- Don't bundle ASM classes (#842603)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Apr 30 2012 Juan Hernandez <juan.hernandez@redhat.com> 1.9.4-3
- Remove the build dependency on maven ant tasks

* Wed Feb 15 2012 Juan Hernandez <juan.hernandez@redhat.com> 1.9.4-2
- Updated license to ASL 2.0 or LGPLv2
- Removed macros from the source URL

* Mon Feb 13 2012 Juan Hernandez <juan.hernandez@redhat.com> 1.9.4-1
- Update to upstream version 1.9.4

* Mon Feb 13 2012 Juan Hernandez <juan.hernandez@redhat.com> 1.6.3-3
- Include jackson-jarxrs.jar in the package

* Mon Feb 13 2012 Juan Hernandez <juan.hernandez@redhat.com> 1.6.3-2
- Don't use absolute references but build-classpath

* Thu Feb 9 2012 Juan Hernandez <juan.hernandez@redhat.com> 1.6.3-1
- Initial packaging

