{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    python3
    python3Packages.pip
    python3Packages.numpy
    python3Packages.pandas
    python3Packages.sympy
    python3Packages.scikit-learn
    python3Packages.jupyter
    python3Packages.matplotlib
    python3Packages.kaggle
    python3Packages.mpmath
  ];

  shellHook = ''
    echo "AIMO Progress Prize 3 environment activated"
    echo "Python packages: numpy, pandas, sympy, scipy, jupyter, matplotlib"
    export PS1="\n\[\033[1;32m\][nix-shell:\w]\$\[\033[0m\] "
  '';
}
