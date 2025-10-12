import argparse
import json
import subprocess
import sys

def get_repository(profile, package, ref) -> str:
    """
    Determine Artifactory repository to which this package needs to be uploaded based on author name.
    """
    process = subprocess.run(["conan", "graph", "info", f"--requires={package}", f"-pr:a={profile}", "--format=json"], capture_output=True)
    if process.returncode != 0:
        print(process.stderr, file=sys.stderr)
        sys.exit(process.returncode)
    graph = json.loads(process.stdout)
    
    # Default repo is external.
    repository = "external"

    # Look for author of package. If me, select internal.
    for index in graph["graph"]["nodes"]:
        if ref == graph["graph"]["nodes"][index]["ref"]:
            if graph["graph"]["nodes"][index]["author"] == "Tim Zoet":
                repository = "internal"
    
    return repository

def build(profile, package):
    req, bld = package["build_args"].split()
    process = subprocess.run(["conan", "install", f"-pr:a={profile}", req, bld])
    if process.returncode != 0:
        print(process.stderr, file=sys.stderr)
        sys.exit(process.returncode)

def upload(profile, package, ref):
    repository = get_repository(profile, package, ref)
    process = subprocess.run(["conan", "upload", "-r", repository, ref])
    if process.returncode != 0:
        print(process.stderr, file=sys.stderr)
        sys.exit(process.returncode)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--profile", required=True, help="Conan profile name")
    parser.add_argument("-u", "--upload", action="store_true", help="Upload to Artifactory")
    parser.add_argument("package")

    args = parser.parse_args()

    process = subprocess.run(["conan", "graph", "build-order", f"--requires={args.package}", f"-pr:a={args.profile}", "--format=json", "--order-by=recipe", "--build=missing", "--reduce"], capture_output=True)
    if process.returncode != 0:
        print(process.stderr, file=sys.stderr)
        sys.exit(process.returncode)
    
    graph = json.loads(process.stdout)
    packages = [package for group in graph["order"] for ref in group for level in ref["packages"] for package in level]
    references = [ref["ref"] for group in graph["order"] for ref in group]

    for package in packages:
        build(args.profile, package)

    if args.upload:
        for ref in references:
            upload(args.profile, args.package, ref)

    sys.exit(0)
