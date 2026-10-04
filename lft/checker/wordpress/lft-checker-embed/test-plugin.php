<?php
/**
 * Stubs just enough WordPress to exercise the plugin's pure logic: path
 * sanitisation (a bad path means a broken rewrite rule), the route table
 * (getting robots or framing the wrong way round would either hide the tool
 * from search or let the embed compete with it), the settings sanitiser, and
 * the shortcode's origin pinning.
 */
define( 'ABSPATH', __DIR__ . '/' );

$GLOBALS['opt']    = array();
$GLOBALS['errors'] = array();

function add_action() {}
function add_filter() {}
function add_shortcode() {}
function register_activation_hook() {}
function register_deactivation_hook() {}
function plugin_dir_path( $f ) { return dirname( $f ) . '/'; }
function get_option( $k, $d = false ) { return $GLOBALS['opt'][ $k ] ?? $d; }
function home_url( $p = '/' ) { return 'https://luggagefortravel.com' . $p; }
function trailingslashit( $s ) { return rtrim( $s, '/' ) . '/'; }
function untrailingslashit( $s ) { return rtrim( $s, '/' ); }
function wp_parse_args( $a, $d = array() ) { return array_merge( $d, (array) $a ); }
function sanitize_text_field( $s ) { return trim( strip_tags( (string) $s ) ); }
function esc_url( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES ); }
function esc_attr( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES ); }
function esc_html( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES ); }
function wp_json_encode( $s ) { return json_encode( $s ); }
function wp_rand( $a, $b ) { return 4242; }
function add_settings_error( $slug, $code, $msg, $type = 'error' ) { $GLOBALS['errors'][] = $code; }
function shortcode_atts( $pairs, $atts, $sc = '' ) {
	$atts = (array) $atts;
	$out  = array();
	foreach ( $pairs as $k => $v ) { $out[ $k ] = array_key_exists( $k, $atts ) ? $atts[ $k ] : $v; }
	return $out;
}

require __DIR__ . '/lft-checker-embed.php';

$pass = 0; $fail = 0;
function ok( $label, $got, $want ) {
	global $pass, $fail;
	if ( $got === $want ) { $pass++; echo "  ok   $label\n"; return; }
	$fail++;
	echo "  FAIL $label\n       got:  " . var_export( $got, true ) . "\n       want: " . var_export( $want, true ) . "\n";
}
function conf( $a ) { $GLOBALS['opt'][ LFTCE_OPTION ] = $a; }
function set_path( $p ) { conf( array( 'path' => $p ) ); }

echo "path sanitisation\n";
$GLOBALS['opt'] = array();
ok( 'default when unset', lftce_path(), 'carry-on-size-checker/embed' );
set_path( 'carry-on-size-checker/embed' );
ok( 'clean path survives', lftce_path(), 'carry-on-size-checker/embed' );
set_path( '/carry-on-size-checker/embed/' );
ok( 'slashes trimmed', lftce_path(), 'carry-on-size-checker/embed' );
set_path( 'Carry-On-Size-Checker/EMBED' );
ok( 'lowercased', lftce_path(), 'carry-on-size-checker/embed' );
set_path( 'checker//embed///x' );
ok( 'double slashes collapsed', lftce_path(), 'checker/embed/x' );
set_path( 'embed.*' );
ok( 'regex metachars stripped, not escaped', lftce_path(), 'embed' );
set_path( 'a$b^c(d)e[f]g|h+i?j' );
ok( 'every metachar stripped', lftce_path(), 'abcdefghij' );
set_path( '' );
ok( 'empty falls back', lftce_path(), 'carry-on-size-checker/embed' );
set_path( '///' );
ok( 'slashes-only falls back', lftce_path(), 'carry-on-size-checker/embed' );
set_path( '../../wp-config' );
ok( 'traversal reduced to a flat segment', lftce_path(), 'wp-config' );

echo "\nthe rewrite regexes the paths produce\n";
$GLOBALS['opt'] = array();
$re = '#^' . lftce_path() . '/?$#';
ok( 'matches the bare embed path', (bool) preg_match( $re, 'carry-on-size-checker/embed' ), true );
ok( 'matches with trailing slash', (bool) preg_match( $re, 'carry-on-size-checker/embed/' ), true );
ok( 'does not match a child', (bool) preg_match( $re, 'carry-on-size-checker/embed/x' ), false );
ok( 'does not match a prefix sibling', (bool) preg_match( $re, 'carry-on-size-checker/embedded' ), false );
$main_re = '#^' . lftce_main_path() . '/?$#';
ok( 'the embed rule ignores the main path', (bool) preg_match( $re, lftce_main_path() ), false );
ok( 'the main rule ignores the embed path', (bool) preg_match( $main_re, lftce_path() ), false );

echo "\nurls\n";
ok( 'embed url', lftce_url(), 'https://luggagefortravel.com/carry-on-size-checker/embed/' );
ok( 'main url', lftce_main_url(), 'https://luggagefortravel.com/carry-on-size-checker/' );

echo "\nroute table\n";
$GLOBALS['opt'] = array();
$r = lftce_routes();
ok( 'only the embed by default', array_keys( $r ), array( 'embed' ) );
ok( 'embed is noindex', $r['embed']['robots'], 'noindex, follow' );
ok( 'embed is framable by default', $r['embed']['framable'], true );
ok( 'embed serves embed.html', basename( $r['embed']['file'] ), 'embed.html' );

conf( array( 'allow_framing' => 0 ) );
$r = lftce_routes();
ok( 'framing can be turned off', $r['embed']['framable'], false );
ok( 'but it stays noindex', $r['embed']['robots'], 'noindex, follow' );

conf( array( 'serve_main' => 1 ) );
$r = lftce_routes();
ok( 'both routes once main is on', array_keys( $r ), array( 'embed', 'main' ) );
ok( 'main serves checker.html', basename( $r['main']['file'] ), 'checker.html' );
ok( 'main is indexable, NOT noindex', $r['main']['robots'], '' );
ok( 'main is not opened up to third-party framing', $r['main']['framable'], false );
ok( 'the embed is still noindex alongside it', $r['embed']['robots'], 'noindex, follow' );
ok( 'the embed is still framable alongside it', $r['embed']['framable'], true );
ok( 'the embed is registered first', array_key_first( $r ), 'embed' );

conf( array( 'serve_main' => 1, 'path' => 'x/y', 'main_path' => 'x/y' ) );
$r = lftce_routes();
ok( 'one path cannot serve two documents', array_keys( $r ), array( 'embed' ) );

echo "\nsettings sanitiser\n";
$GLOBALS['errors'] = array();
$s = lftce_sanitize( array( 'path' => 'x/y', 'allow_framing' => '1', 'max_age' => '600' ) );
ok( 'framing on', $s['allow_framing'], 1 );
ok( 'max_age cast', $s['max_age'], 600 );
$s = lftce_sanitize( array() );
ok( 'framing off when the box is unticked', $s['allow_framing'], 0 );
ok( 'main off when the box is unticked', $s['serve_main'], 0 );
ok( 'max_age defaults', $s['max_age'], 3600 );
$s = lftce_sanitize( array( 'max_age' => '-50' ) );
ok( 'negative max_age floored', $s['max_age'], 0 );
$s = lftce_sanitize( array( 'max_age' => '99999999' ) );
ok( 'max_age capped at a week', $s['max_age'], 604800 );
$GLOBALS['errors'] = array();
$s = lftce_sanitize( array( 'serve_main' => '1', 'path' => 'same', 'main_path' => 'same' ) );
ok( 'colliding paths force main off', $s['serve_main'], 0 );
ok( 'and say so', $GLOBALS['errors'], array( 'lftce_same_path' ) );
$s = lftce_sanitize( array( 'path' => 'A B/../C!' ) );
ok( 'the stored path is already clean', $s['path'], 'ab/c' );

echo "\nshortcode\n";
$GLOBALS['opt'] = array();
$out = lftce_shortcode( array() );
ok( 'iframe points at the embed URL', (bool) strpos( $out, 'src="https://luggagefortravel.com/carry-on-size-checker/embed/"' ), true );
ok( 'default height', (bool) strpos( $out, 'height="900"' ), true );
ok( 'lazy loaded', (bool) strpos( $out, 'loading="lazy"' ), true );
// wp_json_encode escapes forward slashes; "https:\/\/x" === "https://x" in JS, and the
// escaping is what keeps a URL from closing the script block.
ok( 'origin is pinned', (bool) strpos( $out, 'e.origin!==' . wp_json_encode( 'https://luggagefortravel.com' ) ), true );
ok( 'origin is not a wildcard', (bool) strpos( $out, 'e.origin!=="*"' ), false );
ok( 'listens for the documented message type', (bool) strpos( $out, 'lft-checker-height' ), true );
$out = lftce_shortcode( array( 'height' => '600"><script>bad()</script>' ) );
ok( 'height is cast to int, so markup cannot be injected', (bool) strpos( $out, 'height="600"' ), true );
ok( 'no injected script survived', (bool) strpos( $out, 'bad()' ), false );
$out = lftce_shortcode( array( 'title' => 'A "quoted" title' ) );
ok( 'title attribute escaped', (bool) strpos( $out, 'title="A &quot;quoted&quot; title"' ), true );

echo "\nbundled files\n";
$embed   = LFTCE_DIR . 'embed.html';
$checker = LFTCE_DIR . 'checker.html';
ok( 'embed.html bundled', is_readable( $embed ), true );
ok( 'checker.html bundled', is_readable( $checker ), true );
$e = file_get_contents( $embed );
$c = file_get_contents( $checker );
ok( 'embed is the widget', (bool) strpos( $e, 'lft-checker-height' ), true );
ok( 'embed is noindex in the markup too', (bool) strpos( $e, 'name="robots" content="noindex, follow"' ), true );
ok( 'embed canonicals to the parent', (bool) strpos( $e, 'rel="canonical" href="https://luggagefortravel.com/carry-on-size-checker/"' ), true );
ok( 'checker is indexable in the markup', (bool) strpos( $c, 'name="robots" content="index, follow"' ), true );
ok( 'checker is self-canonical', (bool) strpos( $c, 'rel="canonical" href="https://luggagefortravel.com/carry-on-size-checker/"' ), true );
ok( 'checker carries its own chrome', (bool) strpos( $c, 'class="site-header"' ), true );
ok( 'embed strips that chrome', (bool) strpos( $e, 'class="site-header"' ), false );
ok( 'checker ships the embed code box', (bool) strpos( $c, 'id="embedCode"' ), true );
ok( 'embed does not nest one', (bool) strpos( $e, 'id="embedCode"' ), false );
ok( 'the embed box advertises the served path', (bool) strpos( $c, 'luggagefortravel.com/' . lftce_path() . '/' ), true );

echo "\n$pass passed, $fail failed\n";
exit( $fail > 0 ? 1 : 0 );
