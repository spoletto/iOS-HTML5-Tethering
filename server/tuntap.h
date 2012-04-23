/*
 * The following code was taken from the website given in the handout,
 * http://backreference.org/2010/03/26/tuntap-interface-tutorial/.
 */

#ifndef __TUN_TAP_H__
#define __TUN_TAP_H__

/* Arguments taken by the function:
 *
 * char *dev: the name of an interface (or '\0'). MUST have enough
 *   space to hold the interface name if '\0' is passed
 * int flags: interface flags (eg, IFF_TUN etc.)
 */
int tun_alloc(char *dev, int flags);

#endif