1
git show --pretty=format:"Hash: %H Message: %s" -q aefea
Hash: aefead2207ef7e2aa5dc81a34aedf0cad4c32545 Message: Update CHANGELOG.md

2
git show --pretty=format:"%d" -q 85024d3
(tag: v0.12.23)

3
2 штуки
git show --pretty=format:"%p" -q b8d720
56cd7859e 9ea88f22f

4
git show --pretty=format:"Hash: %H Message: %s" -q v0.12.23...v0.12.24
Hash: 33ff1c03bb960b332be3af2e333462dde88b279e Message: v0.12.24
Hash: b14b74c4939dcab573326f4e3ee2a62e23e12f89 Message: [Website] vmc provider links
Hash: 3f235065b9347a758efadc92295b540ee0a5e26e Message: Update CHANGELOG.md
Hash: 6ae64e247b332925b872447e9ce869657281c2bf Message: registry: Fix panic when server is unreachable
Hash: 5c619ca1baf2e21a155fcdb4c264cc9e24a2a353 Message: website: Remove links to the getting started guide's old location
Hash: 06275647e2b53d97d4f0a19a0fec11f6d69820b5 Message: Update CHANGELOG.md
Hash: d5f9411f5108260320064349b757f55c09bc4b80 Message: command: Fix bug when using terraform login on Windows
Hash: 4b6d06cc5dcb78af637bbb19c198faff37a066ed Message: Update CHANGELOG.md
Hash: dd01a35078f040ca984cdd349f18d0b67e486c35 Message: Update CHANGELOG.md
Hash: 225466bc3e5f35baa5d07197bbc079345b77525e Message: Cleanup after v0.12.23 release

5
git log -S "func providerSource(" --oneline
5af1e6234ab6da412fb8637393c5a17a1b293663

6
git log -L :globalPluginDirs:plugins.go --oneline

7
git log -S "func synchronizedWriters("
Author: Martin Atkins <mart@degeneration.co.uk>
Date:   Wed May 3 16:25:41 2017 -0700
