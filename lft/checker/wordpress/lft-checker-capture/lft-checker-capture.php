<?php
/**
 * Plugin Name:       LFT Checker Capture
 * Description:       Analytics and result-aware email capture for the carry-on size checker. Loads only on the checker page. Ships in preview mode until a Kit form UID is set.
 * Version:           1.0.0
 * Requires at least: 6.0
 * Requires PHP:      7.4
 * Author:            GMK Media Ltd
 * License:           GPL-2.0-or-later
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

define( 'LFTCC_VERSION', '1.0.0' );
define( 'LFTCC_OPTION', 'lftcc_settings' );

/**
 * Settings, with defaults. kit_form_uid empty keeps the block in preview mode:
 * the analytics run and the form validates, but nothing is sent anywhere.
 */
function lftcc_settings() {
	$defaults = array(
		'kit_form_uid' => '',
		'path_match'   => 'carry-on-size-checker',
		'fallback_url' => '',
		'privacy_url'  => '/privacy-policy/',
		'debug'        => 0,
	);
	return wp_parse_args( get_option( LFTCC_OPTION, array() ), $defaults );
}

/**
 * Only load on the checker page. Matching on the request path rather than a post ID
 * keeps this working whether the tool is a page, a template or a static file.
 */
function lftcc_is_checker_page() {
	$s = lftcc_settings();
	$needle = trim( $s['path_match'] );
	if ( '' === $needle ) {
		return false;
	}
	$path = isset( $_SERVER['REQUEST_URI'] ) ? wp_unslash( $_SERVER['REQUEST_URI'] ) : '';
	return false !== strpos( $path, $needle );
}

function lftcc_enqueue() {
	if ( is_admin() || ! lftcc_is_checker_page() ) {
		return;
	}
	$s   = lftcc_settings();
	$dir = plugin_dir_url( __FILE__ ) . 'assets/';

	wp_enqueue_style( 'lftcc', $dir . 'lft-checker-capture.css', array(), LFTCC_VERSION );
	wp_enqueue_script( 'lftcc', $dir . 'lft-checker-capture.js', array(), LFTCC_VERSION, true );

	$config = array(
		'kitFormUid'     => '' !== $s['kit_form_uid'] ? $s['kit_form_uid'] : null,
		'kitFallbackUrl' => '' !== $s['fallback_url'] ? $s['fallback_url'] : home_url( '/' ),
		'privacyUrl'     => $s['privacy_url'],
		'debug'          => (bool) $s['debug'],
	);

	// Printed before the script so the script reads it on first run.
	wp_add_inline_script(
		'lftcc',
		'window.LFT_CHECKER_CONFIG = ' . wp_json_encode( $config ) . ';',
		'before'
	);
}
add_action( 'wp_enqueue_scripts', 'lftcc_enqueue' );

/* -------------------------------------------------------------------------
 * Settings screen
 * ---------------------------------------------------------------------- */

function lftcc_menu() {
	add_options_page(
		'LFT Checker Capture',
		'LFT Checker',
		'manage_options',
		'lftcc',
		'lftcc_settings_page'
	);
}
add_action( 'admin_menu', 'lftcc_menu' );

function lftcc_register() {
	register_setting(
		'lftcc_group',
		LFTCC_OPTION,
		array( 'sanitize_callback' => 'lftcc_sanitize' )
	);
}
add_action( 'admin_init', 'lftcc_register' );

function lftcc_sanitize( $input ) {
	return array(
		'kit_form_uid' => sanitize_text_field( $input['kit_form_uid'] ?? '' ),
		'path_match'   => sanitize_text_field( $input['path_match'] ?? 'carry-on-size-checker' ),
		'fallback_url' => esc_url_raw( $input['fallback_url'] ?? '' ),
		'privacy_url'  => sanitize_text_field( $input['privacy_url'] ?? '/privacy-policy/' ),
		'debug'        => empty( $input['debug'] ) ? 0 : 1,
	);
}

function lftcc_settings_page() {
	if ( ! current_user_can( 'manage_options' ) ) {
		return;
	}
	$s = lftcc_settings();
	$live = '' !== $s['kit_form_uid'];
	?>
	<div class="wrap">
		<h1>LFT Checker Capture</h1>

		<div class="notice notice-<?php echo $live ? 'success' : 'warning'; ?> inline" style="margin:16px 0;padding:10px 14px">
			<p style="margin:0">
				<strong><?php echo $live ? 'Live.' : 'Preview mode.'; ?></strong>
				<?php
				echo $live
					? 'Subscriptions are being sent to Kit.'
					: 'Analytics are running and the form validates, but no addresses are sent anywhere. Add a Kit form UID below to go live.';
				?>
			</p>
		</div>

		<form method="post" action="options.php">
			<?php settings_fields( 'lftcc_group' ); ?>
			<table class="form-table" role="presentation">
				<tr>
					<th scope="row"><label for="lftcc_uid">Kit form UID</label></th>
					<td>
						<input name="<?php echo esc_attr( LFTCC_OPTION ); ?>[kit_form_uid]" id="lftcc_uid"
						       type="text" class="regular-text" value="<?php echo esc_attr( $s['kit_form_uid'] ); ?>">
						<p class="description">The number in your Kit embed code. Leave empty to stay in preview mode.</p>
					</td>
				</tr>
				<tr>
					<th scope="row"><label for="lftcc_path">Load on URLs containing</label></th>
					<td>
						<input name="<?php echo esc_attr( LFTCC_OPTION ); ?>[path_match]" id="lftcc_path"
						       type="text" class="regular-text" value="<?php echo esc_attr( $s['path_match'] ); ?>">
						<p class="description">Nothing is loaded on any other page.</p>
					</td>
				</tr>
				<tr>
					<th scope="row"><label for="lftcc_fallback">Signup fallback URL</label></th>
					<td>
						<input name="<?php echo esc_attr( LFTCC_OPTION ); ?>[fallback_url]" id="lftcc_fallback"
						       type="url" class="regular-text" value="<?php echo esc_attr( $s['fallback_url'] ); ?>"
						       placeholder="<?php echo esc_attr( home_url( '/cheat-sheet/' ) ); ?>">
						<p class="description">Where a visitor is sent if the subscription request fails.</p>
					</td>
				</tr>
				<tr>
					<th scope="row"><label for="lftcc_privacy">Privacy policy URL</label></th>
					<td>
						<input name="<?php echo esc_attr( LFTCC_OPTION ); ?>[privacy_url]" id="lftcc_privacy"
						       type="text" class="regular-text" value="<?php echo esc_attr( $s['privacy_url'] ); ?>">
					</td>
				</tr>
				<tr>
					<th scope="row">Debug</th>
					<td>
						<label>
							<input name="<?php echo esc_attr( LFTCC_OPTION ); ?>[debug]" type="checkbox"
							       value="1" <?php checked( 1, (int) $s['debug'] ); ?>>
							Log every event to the browser console
						</label>
						<p class="description">Use this to confirm which hooks matched the live DOM, then turn it off.</p>
					</td>
				</tr>
			</table>
			<?php submit_button(); ?>
		</form>

		<h2>Before you go live</h2>
		<ol>
			<li>Create three custom fields in Kit — <code>airline</code>, <code>verdict</code>, <code>allowance</code> — or they are dropped silently.</li>
			<li>Turn double opt-in on in Kit. The confirmation click is your proof of consent.</li>
			<li>Load the checker with Debug on and run a check. The opt-in block should appear below the verdict.</li>
		</ol>
	</div>
	<?php
}
