{
  description = "This is a very simple AI adventure builder and runner";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = {
    self,
    nixpkgs,
    flake-utils,
  }:
    flake-utils.lib.eachDefaultSystem (system: let
      pkgs = nixpkgs.legacyPackages.${system};
    in {
      packages = rec {
        # Package as library
        ai-textadventure = pkgs.python3.pkgs.buildPythonPackage {
          pname = "ai-textadventure";
          version = "0.0.1";
          format = "pyproject";

          src = ./.;

          propagatedBuildInputs = with pkgs.python3.pkgs; [
            setuptools
            openai
          ];

          meta = with nixpkgs.lib; {
            description = "This is a very simple AI adventure builder";
            homepage = "https://github.com/christ0pher/ai-textadventure";
            license = licenses.gpl3;
          };
        };

        # Streamlit executable
        runner = pkgs.writeShellApplication {
          name = "ai-textadventure-runner";
          runtimeInputs = [pkgs.streamlit];
          text = ''
            export PYTHONPATH=${pkgs.python3.pkgs.makePythonPath [ai-textadventure]}
            streamlit run ${./adventure.py}
          '';
        };

        default = ai-textadventure;
      };

      apps = rec {
        ai-textadventure = {
          description = "This is a very simple AI adventure builder and runner";
          type = "app";
          program = "${pkgs.lib.getExe self.packages.${system}.runner}";
        };

        default = ai-textadventure;
      };

      devShells.default = let
        pyenv = pkgs.python3.withPackages (ps:
          with ps; [
            self.packages.${system}.ai-textadventure
            openai
          ]);
      in
        pkgs.mkShell {
          nativeBuildInputs = with pkgs; [
            pyenv
            streamlit
          ];
        };
    });
}
