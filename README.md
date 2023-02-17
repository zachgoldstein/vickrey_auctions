# Vickrey Auctions with Django & HTMX

This is an application to facilitate vickrey-style auctions.

Inspired by https://kevinlynagh.com/notes/pricing-niche-products/

A Vickrey auction is a closed-bid type of auction for small numbers of items. Example is a really small run of mechanical keyboards:

- You make 10 really cool keyboards, 1000 people are interested in them. How much do you sell them for?
- Ask everybody to bid what they would pay for the keyboards
- The top 10 bids all pay the 11th highest price

The application is built with:
- django
- htmx
- tailwindcss
- shoelace UI components

A secondary goal is explore what building a full application looks like with minimal javascript tooling. This is a testbed to find friction points with django & htmx, and to learn more about what the developer experience looks like for a traditional CRUD application built with these tools.

See https://github.com/zachgoldstein/vickrey_auctions/wiki for more details!
