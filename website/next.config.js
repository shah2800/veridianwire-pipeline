/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  images: {
    remotePatterns: [
      { protocol: 'https', hostname: '**' },
    ],
  },
  cacheMaxMemorySize: 52 * 1024 * 1024,
}

module.exports = nextConfig
