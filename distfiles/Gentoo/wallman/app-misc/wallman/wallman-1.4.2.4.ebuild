# Copyright 1999-2024 Gentoo Authors
# Distributed under the terms of the MIT License

EAPI=8

DISTUTILS_USE_PEP517=setuptools
PYTHON_COMPAT=( python3_{11,12} )
inherit distutils-r1 pypi

DESCRIPTION="A python program that sets dynamic wallpapers on minimalistic Window Managers."
HOMEPAGE="https://git.entheuer.de/emma/wallman/"
SRC_URI="$(pypi_sdist_url "${PN^}" "${PV}")"

LICENSE="MIT"
SLOT="0"
KEYWORDS="~amd64 ~x86"

RDEPEND="
	dev-python/APScheduler[${PYTHON_USEDEP}]
	dev-python/pillow[${PYTHON_USEDEP}]
	dev-python/pystray[${PYTHON_USEDEP}]
	media-gfx/feh
	x11-libs/libnotify
"

BDEPEND="
	dev-python/setuptools[${PYTHON_USEDEP}]
	dev-python/wheel[${PYTHON_USEDEP}]
	dev-python/certifi[${PYTHON_USEDEP}]
"

src_prepare() {
	distutils-r1_python_prepare_all
}

#src_prepare() {
#	mv src/* . || die "Failed to move source files"
#}
python_compile() {
	distutils-r1_python_compile -j1
}
python_install() {
	distutils-r1_python_install
	# Add a symlink to make the script callable from the commandline
	local scriptname="wallman.py"
	local target="/usr/bin/wallman"
	local scriptpath="$(python_get_sitedir)/${scriptname}"
	fperms +x "${scriptpath}"
	dosym "${scriptpath}" "${target}"
	# Copy files into /etc/wallman
	dodir /etc/wallman
	insinto /etc/wallman
	newins "${S}/sample_config.toml" "wallman.toml"
	doins -r "${S}/icons/" "icons/"
	# Create logfile directory
	dodir /var/log/wallman
	keepdir /var/log/wallman
	fperms 0733 /var/log/wallman
	# Copy .desktop file into the appropriate location
	insinto /usr/share/applications
	newins "${S}/distfiles/wallman.desktop" "wallman.desktop"
}

#src_install() {
#}

pkg_postinst() {
	elog "Wallman has been installed. A sample configuration file called wallman.toml is located in /etc/wallman. Copy that file into ~/.config/wallman/wallman.toml to configure wallman."
	elog "A log file for Wallman can be found in /etc/log/wallman"
}
