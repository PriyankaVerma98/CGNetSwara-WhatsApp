# WhatsApp-Swara
Use of WhatsApp to receive and disseminate content for CGNet Swara portal

` function if\_audio (\$content) \{ \\
global \$postings; \\
global \$currentid;\\
if (!veryempty(\$postings[\$currentid]['audio\_file'])) \{ \\
        return trim(fullparse (stripcontainer(\$content))); \\
    \} else \{ return ``"; \} \\ 
\}
`
------
#### Online Resources
- [Php basics](https://www.smashingmagazine.com/2010/04/php-what-you-need-to-know-to-play-with-the-web/)
- [PhP variables scope](http://cs.ucf.edu/~mikel/Telescopes/scope.htm)
- [HTTP POST request](https://reqbin.com/Article/HttpPost)
- [Apache Web server](https://www.hostinger.in/tutorials/what-is-apache)
