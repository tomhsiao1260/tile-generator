import {
	DebugTilesRenderer as TilesRenderer,
} from './three/DebugTilesRenderer.js';
import {
	Scene,
	DirectionalLight,
	AmbientLight,
	WebGLRenderer,
	PerspectiveCamera,
	Group,
	sRGBEncoding,
	FogExp2,
	MeshBasicMaterial
} from 'three';
import { FlyOrbitControls } from './FlyOrbitControls.js';
import { GUI } from 'three/examples/jsm/libs/lil-gui.module.min.js';

let camera, controls, scene, renderer;
let groundTiles;

const params = {

	errorTarget: 12,
	displayBoxBounds: false,
	fog: false,

};

init();
render();

function init() {

	const fog = new FogExp2( 0xd8cec0, .0075, 250 );
	scene = new Scene();

	// primary camera view
	renderer = new WebGLRenderer( { antialias: true } );
	renderer.setPixelRatio( window.devicePixelRatio );
	renderer.setSize( window.innerWidth, window.innerHeight );
	renderer.setClearColor( 0xd8cec0 );
	renderer.outputEncoding = sRGBEncoding;

	document.body.appendChild( renderer.domElement );
	renderer.domElement.tabIndex = 1;

	camera = new PerspectiveCamera( 60, window.innerWidth / window.innerHeight, 0.0001, 500 );
	camera.position.set( 0, 10, 30 );

	// controls
	controls = new FlyOrbitControls( camera, renderer.domElement );
	controls.screenSpacePanning = false;
	controls.minDistance = 1;
	controls.maxDistance = 2000;
	controls.maxPolarAngle = Math.PI / 2;
	controls.baseSpeed = 0.1;
	controls.fastSpeed = 0.2;

	// lights
	const dirLight = new DirectionalLight( 0xffffff );
	dirLight.position.set( 1, 2, 3 );
	scene.add( dirLight );

	const ambLight = new AmbientLight( 0xffffff, 0.2 );
	scene.add( ambLight );

	const tilesParent = new Group();
	tilesParent.rotation.set( Math.PI / 2, 0, 0 );
	scene.add( tilesParent );

	groundTiles = new TilesRenderer( '/tileset.json' );
	// groundTiles = new TilesRenderer( 'https://raw.githubusercontent.com/NASA-AMMOS/3DTilesSampleData/master/msl-dingo-gap/0528_0260184_to_s64o256_colorize/0528_0260184_to_s64o256_colorize/0528_0260184_to_s64o256_colorize_tileset.json' );
	groundTiles.fetchOptions.mode = 'cors';
	groundTiles.lruCache.minSize = 900;
	groundTiles.lruCache.maxSize = 1300;
	groundTiles.errorTarget = 12;

	tilesParent.add( groundTiles.group );

	groundTiles.onLoadModel = function ( scene ) {
		// create a custom material for the tile
		scene.traverse( c => {

			if ( c.material ) {
				let batchTableObject = c;
				while ( ! batchTableObject.batchTable ) {
					batchTableObject = batchTableObject.parent;
				}

				const value = batchTableObject.batchTable.header.intensity;
				const color = value * 255;
				const hexColor = color << 16 | color << 8 | color; 
	
				c.originalMaterial = c.material;
				c.material = new MeshBasicMaterial({ color: hexColor });
	
			}

		} );
	
	};

	onWindowResize();
	window.addEventListener( 'resize', onWindowResize, false );

	const gui = new GUI();
	gui.add( params, 'fog' ).onChange( v => {

		scene.fog = v ? fog : null;

	} );

	gui.add( params, 'displayBoxBounds' );
	gui.add( params, 'errorTarget', 0, 100 );
	gui.open();

}

function onWindowResize() {

	camera.aspect = window.innerWidth / window.innerHeight;
	camera.updateProjectionMatrix();
	renderer.setSize( window.innerWidth, window.innerHeight );
	renderer.setPixelRatio( window.devicePixelRatio );

}

function render() {

	requestAnimationFrame( render );

	camera.updateMatrixWorld();

	groundTiles.errorTarget = params.errorTarget;
	groundTiles.displayBoxBounds = params.displayBoxBounds;

	groundTiles.setCamera( camera );
	groundTiles.setResolutionFromRenderer( camera, renderer );
	groundTiles.update();

	renderer.render( scene, camera );

}