/** @type {import('next').NextConfig} */
const nextConfig = {
  typescript: {
    ignoreBuildErrors: true,
  },
  experimental: {
    appDir: true,
  },
  images: {
    domains: ['localhost'],
  },
};

module.exports = nextConfig;