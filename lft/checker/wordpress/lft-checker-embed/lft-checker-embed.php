<?php
/**
 * Plugin Name:       LFT Carry-On Checker
 * Description:       Serves the carry-on size checker as a standalone document — the embeddable widget at /carry-on-size-checker/embed/, and optionally the full tool at /carry-on-size-checker/. Sends the right robots and framing headers for each, and includes a diagnostic that tells you whether third-party framing actually works on your host.
 * Version:           1.0.0
 * Requires at least: 6.0
 * Requires PHP:      7.4
 * Author:            GMK Media Ltd
 * License:           GPL-2.0-or-later
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

define( 'LFTCE_VERSION', '1.0.0' );
define( 'LFTCE_OPTION', 'lftce_settings' );
define( 'LFTCE_QV', 'lftce_route' );
define( 'LFTCE_DIR', plugin_dir_path( __FILE__ ) );

/* -------------------------------------------------------------------------
 * Settings
 * ---------------------------------------------------------------------- */

function lftce_settings() {
	$defaults = array(
		'path'          => 'carry-on-size-checker/embed',
		'allow_framing' => 1,
		'serve_main'    => 0,
		'main_path'     => 'carry-on-size-checker',
		'max_age'       => 3600,
	);
	return wp_parse_args( get_option( LFTCE_OPTION, array() ), $defaults );
}

/**
 * Reduces a path to characters that are safe to drop straight into a rewrite
 * regex. Anything else is stripped rather than escaped, so a typo in the settings
 * field can never widen the rule.
 */
function lftce_clean_path( $p, $fallback ) {
	$p = strtolower( (string) $p );
	$p = preg_replace( '#[^a-z0-9/_-]#', '', $p );
	$p = preg_replace( '#/+#', '/', (string) $p );
	$p = trim( (string) $p, '/' );
	return '' === $p ? $fallback : $p;
}

function lftce_path() {
	return lftce_clean_path( lftce_settings()['path'], 'carry-on-size-checker/embed' );
}

function lftce_main_path() {
	return lftce_clean_path( lftce_settings()['main_path'], 'carry-on-size-checker' );
}

function lftce_url() {
	return home_url( '/' . lftce_path() . '/' );
}

function lftce_main_url() {
	return home_url( '/' . lftce_main_path() . '/' );
}

/**
 * The routes this plugin owns, in match order. The embed is registered first so
 * that even if a future path made the two rules overlap, the narrower one wins.
 *
 * The embed is noindex and framable by anyone; the main tool is indexable and
 * left on the site's own framing policy. Getting those two the wrong way round
 * would either hide the tool from search or let the embed compete with it.
 */
function lftce_routes() {
	$s = lftce_settings();

	$routes = array(
		'embed' => array(
			'path'     => lftce_path(),
			'file'     => LFTCE_DIR . 'embed.html',
			'robots'   => 'noindex, follow',
			'framable' => ! empty( $s['allow_framing'] ),
			'label'    => 'Embeddable widget',
		),
	);

	if ( ! empty( $s['serve_main'] ) && lftce_main_path() !== lftce_path() ) {
		$routes['main'] = array(
			'path'     => lftce_main_path(),
			'file'     => LFTCE_DIR . 'checker.html',
			'robots'   => '',
			'framable' => false,
			'label'    => 'Full checker page',
		);
	}

	return $routes;
}

/* -------------------------------------------------------------------------
 * Routing
 * ---------------------------------------------------------------------- */

function lftce_rewrites() {
	foreach ( lftce_routes() as $key => $r ) {
		add_rewrite_rule( '^' . $r['path'] . '/?$', 'index.php?' . LFTCE_QV . '=' . $key, 'top' );
	}
}
add_action( 'init', 'lftce_rewrites' );

function lftce_query_vars( $vars ) {
	$vars[] = LFTCE_QV;
	return $vars;
}
add_filter( 'query_vars', 'lftce_query_vars' );

function lftce_activate() {
	lftce_rewrites();
	flush_rewrite_rules();
}
register_activation_hook( __FILE__, 'lftce_activate' );

function lftce_deactivate() {
	flush_rewrite_rules();
}
register_deactivation_hook( __FILE__, 'lftce_deactivate' );

// A changed path or a newly enabled route needs the rules rebuilt, or the old URL
// keeps serving and the new one 404s.
function lftce_flush_on_save() {
	lftce_rewrites();
	flush_rewrite_rules();
}
add_action( 'update_option_' . LFTCE_OPTION, 'lftce_flush_on_save' );

/* -------------------------------------------------------------------------
 * Serving
 *
 * Priority 0 on template_redirect puts this ahead of redirect_canonical (10),
 * so WordPress never gets the chance to bounce or 404 the URL.
 * ---------------------------------------------------------------------- */

function lftce_maybe_serve() {
	$key    = (string) get_query_var( LFTCE_QV );
	$routes = lftce_routes();
	if ( '' === $key || ! isset( $routes[ $key ] ) ) {
		return;
	}
	$r = $routes[ $key ];

	if ( ! is_readable( $r['file'] ) ) {
		status_header( 500 );
		header( 'Content-Type: text/plain; charset=utf-8' );
		echo 'LFT checker: ' . esc_html( basename( $r['file'] ) ) . " is missing from the plugin folder.\n";
		exit;
	}

	// The query matched a rewrite rule but resolves to no post, so WP has already
	// flagged a 404. Undo that before anything is sent.
	global $wp_query;
	if ( $wp_query instanceof WP_Query ) {
		$wp_query->is_404 = false;
	}
	status_header( 200 );

	$s = lftce_settings();

	// Only PHP-set headers can be removed here. A header added by nginx or Apache
	// survives this, which is exactly what the diagnostic on the settings page is for.
	header_remove( 'Pragma' );
	header_remove( 'Expires' );

	header( 'Content-Type: text/html; charset=' . get_option( 'blog_charset', 'UTF-8' ), true );
	header( 'X-Content-Type-Options: nosniff', true );

	if ( '' !== $r['robots'] ) {
		header( 'X-Robots-Tag: ' . $r['robots'], true );
	}

	if ( $r['framable'] ) {
		header_remove( 'X-Frame-Options' );
		header_remove( 'Content-Security-Policy' );
		header( 'Content-Security-Policy: frame-ancestors *', true );
	}

	$max_age = max( 0, (int) $s['max_age'] );
	header( 'Cache-Control: public, max-age=' . $max_age, true );

	$etag = '"' . md5( LFTCE_VERSION . $key . filemtime( $r['file'] ) . filesize( $r['file'] ) . (int) $r['framable'] ) . '"';
	header( 'ETag: ' . $etag, true );
	header( 'Last-Modified: ' . gmdate( 'D, d M Y H:i:s', filemtime( $r['file'] ) ) . ' GMT', true );

	$inm = isset( $_SERVER['HTTP_IF_NONE_MATCH'] ) ? trim( wp_unslash( $_SERVER['HTTP_IF_NONE_MATCH'] ) ) : '';
	if ( '' !== $inm && $inm === $etag ) {
		status_header( 304 );
		exit;
	}

	header( 'Content-Length: ' . filesize( $r['file'] ), true );
	readfile( $r['file'] );
	exit;
}
add_action( 'template_redirect', 'lftce_maybe_serve', 0 );

/* -------------------------------------------------------------------------
 * Shortcode — [lft_checker_embed] for use on this site
 * ---------------------------------------------------------------------- */

function lftce_shortcode( $atts ) {
	$a = shortcode_atts(
		array(
			'height' => '900',
			'title'  => 'Carry-on size checker',
		),
		$atts,
		'lft_checker_embed'
	);

	$id     = 'lft-checker-' . wp_rand( 1000, 9999 );
	$height = (int) $a['height'];
	$origin = untrailingslashit( home_url( '/' ) );

	$html  = '<iframe id="' . esc_attr( $id ) . '" src="' . esc_url( lftce_url() ) . '"';
	$html .= ' width="100%" height="' . esc_attr( (string) $height ) . '" loading="lazy"';
	$html .= ' title="' . esc_attr( $a['title'] ) . '"';
	$html .= ' style="border:1px solid #e2e8f0;border-radius:8px"></iframe>';

	// Same protocol the public embed snippet documents, with the origin pinned.
	$html .= '<script>(function(){var f=document.getElementById(' . wp_json_encode( $id ) . ');'
		. 'addEventListener("message",function(e){if(e.origin!==' . wp_json_encode( $origin ) . ')return;'
		. 'if(e.data&&e.data.type==="lft-checker-height"&&f)f.style.height=e.data.height+"px";});})();</script>';

	return $html;
}
add_shortcode( 'lft_checker_embed', 'lftce_shortcode' );

/* -------------------------------------------------------------------------
 * Settings screen
 * ---------------------------------------------------------------------- */

function lftce_menu() {
	add_options_page( 'LFT Carry-On Checker', 'LFT Checker Pages', 'manage_options', 'lftce', 'lftce_settings_page' );
}
add_action( 'admin_menu', 'lftce_menu' );

function lftce_register() {
	register_setting( 'lftce_group', LFTCE_OPTION, array( 'sanitize_callback' => 'lftce_sanitize' ) );
}
add_action( 'admin_init', 'lftce_register' );

function lftce_sanitize( $input ) {
	$path = lftce_clean_path( $input['path'] ?? '', 'carry-on-size-checker/embed' );
	$main = lftce_clean_path( $input['main_path'] ?? '', 'carry-on-size-checker' );

	// The same path cannot serve two different documents. Refusing here is better
	// than registering two rules where only the first ever matches.
	$serve_main = empty( $input['serve_main'] ) ? 0 : 1;
	if ( $path === $main ) {
		$serve_main = 0;
		add_settings_error(
			LFTCE_OPTION,
			'lftce_same_path',
			'The embed and the full checker cannot share a path. Serving the full checker was left off.',
			'error'
		);
	}

	return array(
		'path'          => $path,
		'allow_framing' => empty( $input['allow_framing'] ) ? 0 : 1,
		'serve_main'    => $serve_main,
		'main_path'     => $main,
		'max_age'       => max( 0, min( 604800, (int) ( $input['max_age'] ?? 3600 ) ) ),
	);
}

/**
 * Asks a live URL what it actually returns. A loopback request does not always
 * traverse the same CDN or reverse proxy an outside visitor hits, so a clean
 * result here is necessary but not sufficient — hence the note in the output.
 */
function lftce_probe( $url ) {
	$r = wp_remote_get(
		add_query_arg( 'lftce_probe', time(), $url ),
		array(
			'timeout'     => 10,
			'redirection' => 2,
			'headers'     => array( 'Cache-Control' => 'no-cache' ),
		)
	);

	if ( is_wp_error( $r ) ) {
		return array( 'error' => $r->get_error_message() );
	}

	$h = wp_remote_retrieve_headers( $r );
	if ( is_object( $h ) && method_exists( $h, 'getAll' ) ) {
		$h = $h->getAll();
	}
	$h = array_change_key_case( (array) $h, CASE_LOWER );

	$get = function ( $k ) use ( $h ) {
		if ( ! isset( $h[ $k ] ) ) {
			return '';
		}
		return is_array( $h[ $k ] ) ? implode( ', ', $h[ $k ] ) : (string) $h[ $k ];
	};

	$body = wp_remote_retrieve_body( $r );

	return array(
		'status' => (int) wp_remote_retrieve_response_code( $r ),
		'xfo'    => $get( 'x-frame-options' ),
		'csp'    => $get( 'content-security-policy' ),
		'robots' => $get( 'x-robots-tag' ),
		'ctype'  => $get( 'content-type' ),
		'bytes'  => strlen( $body ),
		'is_app' => ( false !== strpos( $body, 'lft-checker-height' ) || false !== strpos( $body, 'id="checkBtn"' ) ),
	);
}

function lftce_render_probe( $probe, $expect_framable ) {
	if ( isset( $probe['error'] ) ) {
		echo '<div class="notice notice-error inline" style="padding:10px 14px"><p style="margin:0">Request failed: <code>'
			. esc_html( $probe['error'] )
			. '</code>. Some hosts block loopback requests; in that case test by framing the URL from another domain.</p></div>';
		return;
	}

	$blocked = '' !== $probe['xfo']
		|| ( '' !== $probe['csp'] && false === strpos( $probe['csp'], 'frame-ancestors *' ) );
	$ok = 200 === $probe['status'] && $probe['is_app'] && ( ! $expect_framable || ! $blocked );
	?>
	<div class="notice notice-<?php echo $ok ? 'success' : 'error'; ?> inline" style="padding:10px 14px">
		<p style="margin:0"><strong>
			<?php
			if ( $ok && $expect_framable ) {
				echo 'Framable. Nothing is blocking the embed.';
			} elseif ( $ok ) {
				echo 'Serving correctly.';
			} elseif ( 200 !== $probe['status'] ) {
				echo 'Returned ' . (int) $probe['status'] . ' — go to Settings &rsaquo; Permalinks and hit Save to rebuild the rewrite rules.';
			} elseif ( ! $probe['is_app'] ) {
				echo 'The URL responded, but the body is not the checker — something else owns this path.';
			} else {
				echo 'A server-level header is blocking framing. Ask your host to drop it on this path.';
			}
			?>
		</strong></p>
	</div>
	<table class="widefat striped" style="max-width:860px;margin-bottom:10px">
		<tbody>
			<tr><td style="width:230px"><strong>HTTP status</strong></td><td><code><?php echo (int) $probe['status']; ?></code></td></tr>
			<tr><td><strong>X-Frame-Options</strong></td><td>
				<?php
				if ( '' === $probe['xfo'] ) {
					echo $expect_framable ? '<em>absent &mdash; good</em>' : '<em>absent</em>';
				} else {
					echo '<code>' . esc_html( $probe['xfo'] ) . '</code>';
					echo $expect_framable ? ' &mdash; <strong>this blocks embedding</strong>' : '';
				}
				?>
			</td></tr>
			<tr><td><strong>Content-Security-Policy</strong></td><td><?php echo '' === $probe['csp'] ? '<em>absent</em>' : '<code>' . esc_html( $probe['csp'] ) . '</code>'; ?></td></tr>
			<tr><td><strong>X-Robots-Tag</strong></td><td><?php echo '' === $probe['robots'] ? '<em>absent</em>' : '<code>' . esc_html( $probe['robots'] ) . '</code>'; ?></td></tr>
			<tr><td><strong>Content-Type</strong></td><td><code><?php echo esc_html( $probe['ctype'] ); ?></code></td></tr>
			<tr><td><strong>Body</strong></td><td><?php echo esc_html( size_format( (int) $probe['bytes'] ) ); ?><?php echo $probe['is_app'] ? ' &mdash; the checker' : ' &mdash; <strong>not the checker</strong>'; ?></td></tr>
		</tbody>
	</table>
	<?php
}

function lftce_settings_page() {
	if ( ! current_user_can( 'manage_options' ) ) {
		return;
	}
	$s      = lftce_settings();
	$routes = lftce_routes();

	$probe = array();
	if ( isset( $_GET['lftce_test'] ) && check_admin_referer( 'lftce_test' ) ) {
		foreach ( $routes as $k => $r ) {
			$probe[ $k ] = lftce_probe( home_url( '/' . $r['path'] . '/' ) );
		}
	}

	$clash = get_page_by_path( lftce_main_path() );
	?>
	<div class="wrap">
		<h1>LFT Carry-On Checker</h1>

		<table class="widefat striped" style="max-width:860px;margin:16px 0">
			<thead><tr><th>Serving</th><th>URL</th><th>Robots</th><th>Framing</th><th>Size</th></tr></thead>
			<tbody>
			<?php foreach ( $routes as $r ) : ?>
				<tr>
					<td><strong><?php echo esc_html( $r['label'] ); ?></strong></td>
					<td><a href="<?php echo esc_url( home_url( '/' . $r['path'] . '/' ) ); ?>" target="_blank" rel="noopener"><code>/<?php echo esc_html( $r['path'] ); ?>/</code></a></td>
					<td><code><?php echo esc_html( '' === $r['robots'] ? 'index, follow' : $r['robots'] ); ?></code></td>
					<td><?php echo $r['framable'] ? 'any site' : 'site policy'; ?></td>
					<td>
						<?php
						echo is_readable( $r['file'] )
							? esc_html( size_format( filesize( $r['file'] ) ) )
							: '<strong style="color:#b32d2e">missing</strong>';
						?>
					</td>
				</tr>
			<?php endforeach; ?>
			<?php if ( ! isset( $routes['main'] ) ) : ?>
				<tr><td colspan="5"><em>The full checker page is not being served by this plugin. Turn it on below if <code>/<?php echo esc_html( lftce_main_path() ); ?>/</code> should serve the bundled version.</em></td></tr>
			<?php endif; ?>
			</tbody>
		</table>

		<form method="post" action="options.php">
			<?php settings_fields( 'lftce_group' ); ?>

			<h2>The embeddable widget</h2>
			<table class="form-table" role="presentation">
				<tr>
					<th scope="row"><label for="lftce_path">Serve at</label></th>
					<td>
						<code><?php echo esc_html( trailingslashit( home_url( '/' ) ) ); ?></code>
						<input name="<?php echo esc_attr( LFTCE_OPTION ); ?>[path]" id="lftce_path" type="text"
						       class="regular-text" value="<?php echo esc_attr( $s['path'] ); ?>">
						<p class="description">
							Lowercase letters, numbers, hyphens and slashes only. This URL is baked into every
							embed code already out in the wild, so set it once and leave it.
						</p>
					</td>
				</tr>
				<tr>
					<th scope="row">Third-party framing</th>
					<td>
						<label>
							<input name="<?php echo esc_attr( LFTCE_OPTION ); ?>[allow_framing]" type="checkbox"
							       value="1" <?php checked( 1, (int) $s['allow_framing'] ); ?>>
							Allow any site to embed the widget
						</label>
						<p class="description">
							Sends <code>frame-ancestors *</code> and strips any <code>X-Frame-Options</code> set by
							PHP. Untick to lock the widget to this domain — the backlink mechanism stops working
							if you do.
						</p>
					</td>
				</tr>
			</table>

			<h2>The full checker page</h2>
			<p style="max-width:860px">
				The checker is a complete HTML document with its own header, footer and navigation, so it
				cannot be pasted into a page body. Tick this to have the plugin serve the bundled version
				at the URL below.
			</p>
			<table class="form-table" role="presentation">
				<tr>
					<th scope="row">Serve the full checker</th>
					<td>
						<label>
							<input name="<?php echo esc_attr( LFTCE_OPTION ); ?>[serve_main]" type="checkbox"
							       value="1" <?php checked( 1, (int) $s['serve_main'] ); ?>>
							Serve <code>checker.html</code> at the path below
						</label>
						<?php if ( $clash ) : ?>
							<p class="description" style="color:#b32d2e">
								<strong>There is already a <?php echo esc_html( get_post_type( $clash ) ); ?> at
								<code>/<?php echo esc_html( lftce_main_path() ); ?>/</code>
								(&ldquo;<?php echo esc_html( get_the_title( $clash ) ); ?>&rdquo;).</strong>
								Turning this on shadows it — the plugin answers first and that
								<?php echo esc_html( get_post_type( $clash ) ); ?> becomes unreachable at this URL.
								It is not deleted, and unticking this gives it back.
								<a href="<?php echo esc_url( get_edit_post_link( $clash->ID ) ); ?>">Look at it first &rarr;</a>
							</p>
						<?php endif; ?>
						<p class="description">
							Indexable (<code>index, follow</code>) and left on your site's own framing policy —
							unlike the widget, which is deliberately noindex.
						</p>
					</td>
				</tr>
				<tr>
					<th scope="row"><label for="lftce_main">Serve at</label></th>
					<td>
						<code><?php echo esc_html( trailingslashit( home_url( '/' ) ) ); ?></code>
						<input name="<?php echo esc_attr( LFTCE_OPTION ); ?>[main_path]" id="lftce_main" type="text"
						       class="regular-text" value="<?php echo esc_attr( $s['main_path'] ); ?>">
						<p class="description">Must differ from the widget path above.</p>
					</td>
				</tr>
			</table>

			<h2>Caching</h2>
			<table class="form-table" role="presentation">
				<tr>
					<th scope="row"><label for="lftce_age">Cache for</label></th>
					<td>
						<input name="<?php echo esc_attr( LFTCE_OPTION ); ?>[max_age]" id="lftce_age" type="number"
						       min="0" max="604800" step="60" value="<?php echo esc_attr( (string) $s['max_age'] ); ?>">
						seconds
						<p class="description">Set to 0 while testing. 3600 is sensible once it is live.</p>
					</td>
				</tr>
			</table>
			<?php submit_button(); ?>
		</form>

		<hr>

		<h2>Does framing actually work?</h2>
		<p style="max-width:860px">
			A host that sends <code>X-Frame-Options: DENY</code> from nginx or Apache breaks every embed
			<em>silently</em> — the iframe just renders blank on the other site and nobody tells you.
			PHP cannot remove a header set at that level. This asks each live URL what it really returns.
		</p>
		<p>
			<a class="button button-primary"
			   href="<?php echo esc_url( wp_nonce_url( admin_url( 'options-general.php?page=lftce&lftce_test=1' ), 'lftce_test' ) ); ?>">
				Run the test
			</a>
		</p>

		<?php foreach ( $probe as $k => $pr ) : ?>
			<h3><?php echo esc_html( $routes[ $k ]['label'] ); ?> &mdash; <code>/<?php echo esc_html( $routes[ $k ]['path'] ); ?>/</code></h3>
			<?php lftce_render_probe( $pr, ! empty( $routes[ $k ]['framable'] ) ); ?>
		<?php endforeach; ?>

		<?php if ( $probe ) : ?>
			<p class="description" style="max-width:860px">
				These requests came from your own server. A CDN or reverse proxy in front of the site can add
				headers that only an outside visitor sees, so confirm once by framing the widget URL from a
				different domain before you pitch the embed to anyone.
			</p>
		<?php endif; ?>

		<hr>

		<h2>Using the widget on this site</h2>
		<p>Drop <code>[lft_checker_embed]</code> into any page or post. Optional attributes:
		<code>height</code> (default 900), <code>title</code>.</p>

		<h2>If a URL 404s</h2>
		<p>Settings &rsaquo; Permalinks &rsaquo; Save Changes. That rebuilds the rewrite rules. Nothing else is needed.</p>
	</div>
	<?php
}
