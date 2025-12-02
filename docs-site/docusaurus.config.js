const {themes} = require('prism-react-renderer');
const lightCodeTheme = themes.github;
const darkCodeTheme = themes.vsDark;

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Arc Flash Studio',
  tagline: 'Professional Arc Flash Analysis • IEEE 1584-2018 Compliant',
  favicon: 'img/favicon.ico',

  url: 'https://your-username.github.io',
  baseUrl: '/arc-flash-studio/',
  
  organizationName: 'your-github-username',
  projectName: 'arc-flash-studio',

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
          editUrl: 'https://github.com/your-username/arc-flash-studio/tree/main/docs-site/',
        },
        blog: {
          showReadingTime: true,
          blogTitle: 'Development Blog',
          blogDescription: 'Building Arc Flash Studio in public',
        },
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // Announcement bar for important updates
      announcementBar: {
        id: 'support_us',
        content:
          '⭐️ If you find this project useful, give it a star on <a target="_blank" rel="noopener noreferrer" href="https://github.com/your-username/arc-flash-studio">GitHub</a>!',
        backgroundColor: '#2563eb',
        textColor: '#ffffff',
        isCloseable: true,
      },
      
      // Navbar configuration
      navbar: {
        title: 'Arc Flash Studio',
        logo: {
          alt: 'Arc Flash Studio',
          src: 'img/logo.svg',
        },
        hideOnScroll: true,
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'tutorialSidebar',
            position: 'left',
            label: 'Docs',
          },
          {
            to: '/blog', 
            label: 'Blog', 
            position: 'left'
          },
          {
            type: 'search',
            position: 'right',
          },
          {
            href: 'https://github.com/your-username/arc-flash-studio',
            position: 'right',
            className: 'header-github-link',
            'aria-label': 'GitHub repository',
          },
        ],
      },
      
      // Footer configuration
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Documentation',
            items: [
              {
                label: 'Getting Started',
                to: '/docs/intro',
              },
              {
                label: 'API Reference',
                to: '/docs/intro',
              },
              {
                label: 'Examples',
                to: '/docs/intro',
              },
            ],
          },
          {
            title: 'Standards',
            items: [
              {
                label: 'IEEE 1584-2018',
                href: 'https://standards.ieee.org/standard/1584-2018.html',
              },
              {
                label: 'NFPA 70E',
                href: 'https://www.nfpa.org/70E',
              },
              {
                label: 'NEC',
                href: 'https://www.nfpa.org/70',
              },
            ],
          },
          {
            title: 'Community',
            items: [
              {
                label: 'GitHub',
                href: 'https://github.com/your-username/arc-flash-studio',
              },
              {
                label: 'Issues',
                href: 'https://github.com/your-username/arc-flash-studio/issues',
              },
              {
                label: 'Discussions',
                href: 'https://github.com/your-username/arc-flash-studio/discussions',
              },
            ],
          },
        ],
        copyright: `
          <div style="margin-top: 2rem; padding-top: 2rem; border-top: 1px solid rgba(255,255,255,0.1);">
            <p style="margin: 0;">Built with ⚡ by electrical engineers, for electrical engineers</p>
            <p style="margin: 0.5rem 0 0 0; opacity: 0.6;">Copyright © ${new Date().getFullYear()} Arc Flash Studio • MIT Licensed</p>
          </div>
        `,
      },
      
      // Code theme
      prism: {
        theme: lightCodeTheme,
        darkTheme: darkCodeTheme,
        additionalLanguages: ['python', 'bash', 'json'],
      },
      
      // Color mode
      colorMode: {
        defaultMode: 'light',
        disableSwitch: false,
        respectPrefersColorScheme: true,
      },
      
      // Metadata
      metadata: [
        {name: 'keywords', content: 'arc flash, IEEE 1584, electrical safety, power systems, NFPA 70E'},
        {name: 'description', content: 'Open-source arc flash calculator compliant with IEEE 1584-2018'},
      ],
    }),
};

module.exports = config;