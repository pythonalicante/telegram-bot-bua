#!/usr/bin/env python
# -*- coding: utf-8 -*-


catalogBookRegex = r"<label class=\"itemlisting.*\" for=\"(.*)\">\\n<!-- title -->\\n<strong>(.*)<\/strong>\\n<!-- and\/or display linked 880 data -->\\n<!-- and\/or display linked 880 data -->\\n<!-- author -->\\n<br\/>(.*)<!-- and\/or display linked 880 data -->\\n<\/label>"
loanBooksRegex =  r"<td class=\"itemlisting.*\">\s*<input type=\"checkbox\" name=\".*\" id=\"RENEW.*\">\s*<\/td>\s*<td class=\"itemlisting.*\">\s*<label for=\"RENEW.*\">\s*<!-- Print the title, if it exists -->\s*(.*)&nbsp;&nbsp;\s*<!-- Print the author, if it exists -->\s*(.*)\s*<\/label>\s*<\/td>\s*<td class=\"itemlisting.*\" align=\"left\">\s*devoluci.*n:\s*<!-- Print the date due -->\s*<strong>(.*)<\/strong><br>\s*<\/td>"
