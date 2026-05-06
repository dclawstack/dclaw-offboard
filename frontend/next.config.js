/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://dclaw-offboard-backend:8130/:path*',
      },
    ];
  },
};

module.exports = nextConfig;
