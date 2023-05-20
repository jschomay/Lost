{ pkgs }: {
	deps = [
    pkgs.python310Full
    pkgs.replitPackages.prybar-python310
    pkgs.replitPackages.stderred
	];
  env = {
    LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath ([
      # Neded for pandas / numpy
      pkgs.stdenv.cc.cc.lib
      pkgs.zlib
      # Needed for pygame
      pkgs.glib
    ] ++ (with pkgs.xlibs; [ libX11 libXext libXinerama libXcursor libXrandr libXi libXxf86vm ]));

    PYTHONBIN = "${pkgs.python310Full}/bin/python3.10";
    LANG = "en_US.UTF-8";
  };
}