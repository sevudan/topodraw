(function (nx) {
 var Line = nx.geometry.Line;
 var Vector = nx.geometry.Vector;
 // extend link class
 nx.define('MyExtendLink', nx.graphic.Topology.Link, {
     properties: {
         sourcemetric: null,
         targetmetric: null,
         sourcelabel: null,
         targetlabel:null
     },
     view: function(view) {
        view.content.push({
            name: 'source',
            type: 'nx.graphic.Text',
            props: {
                'class': 'sourcelabel',
                'alignment-baseline': 'text-after-edge',
                'text-anchor': 'start'
            }
        }, {
            name: 'target',
            type: 'nx.graphic.Text',
            props: {
                'class': 'targetlabel',
                'alignment-baseline': 'text-after-edge',
                'text-anchor': 'end'
            }
        }, {
            name: 'src_metric',
            type: 'nx.graphic.Text',
            props: {
                'class': 'sourcemetric',
                'alignment-baseline': 'text-after-edge',
                'text-anchor': 'end'
            }
        }, {
            name: 'tgt_metric',
            type: 'nx.graphic.Text',
            props: {
                'class': 'targetmetric',
                'alignment-baseline': 'text-after-edge',
                'text-anchor': 'end'
            }
        });
        return view;
     },
     methods: {
         update: function() {
             this.inherited();
             var el, point;
             var stageScale = this.stageScale();
             var width = (this._width || 1) * (this._stageScale || 1);
             var line = this.reverse() ? this.line().negate() : this.line();

             var angle = line.angle();
             var stageScale = this.stageScale();

             var lineEl = this.view('line');
             var pathEL = this.view('path');
             var newLine = line.pad(22 * stageScale, 22 * stageScale);
             lineEl.sets({
                 x1: newLine.start.x,
                 y1: newLine.start.y,
                 x2: newLine.end.x,
                 y2: newLine.end.y
             });
             pathEL.setStyle('display', 'none');
             lineEl.setStyle('display', 'block');
             lineEl.setStyle('stroke-width', width);

            // pad line
            newLine = newLine.pad(15 * stageScale, 15 * stageScale);
            if (this.sourcelabel()) {
                el = this.view('source');
                var angle=newLine.angle();
                if (!(angle>-90 && angle<90)) {
                  angle=angle+180;
                  newLine = newLine.pad((80+this.sourcelabel.length) * stageScale, (60+this.sourcelabel.length) * stageScale);
                }
                point = newLine.start;
                var x=point.x;
                var y=point.y;
                el.set('x', x);
                el.set('y', y);

                el.set('text', this.sourcelabel().replace(/(^G|T)\D*/gi, "$1"));
                el.set('transform', 'rotate(' + angle + ' ' + x + ',' + y + ')');
                el.setStyle('font-size', 12 * stageScale);
                el.setStyle('font-weight', 'bolder');
            }
            if (this.targetlabel()) {
                el = this.view('target');
                var angle=newLine.angle();
                if (!(angle>-90 && angle<90)) {
                  angle=angle+180;
                  newLine = newLine.pad((26+this.sourcelabel.length) * stageScale, (24+this.sourcelabel.length) * stageScale);
                }
                point = newLine.end;
                var x=point.x;
                var y=point.y;
                el.set('x', x);
                el.set('y', y);
                el.set('text', this.targetlabel().replace(/(^G|T)\D*/gi, "$1"));
                el.set('transform', 'rotate(' + angle + ' ' + x + ',' + y + ')');
                el.setStyle('font-size', 12 * stageScale );
                el.setStyle('font-weight', 'bolder');
            }

            line = line.pad(35 * stageScale, 30 * stageScale);

            if (this.sourcemetric()) {
                el = this.view('src_metric');
                point = line.start;
                el.set('x', point.x);
                el.set('y', point.y + 10);
                el.set('text', this.sourcemetric());
                el.set('transform', 'rotate(' + angle + ' ' + point.x + ',' + point.y + ')');
                el.setStyle('font-size', 12 * stageScale);
                el.setStyle('fill', '#689CD2');
            }

            if (this.targetmetric()) {
                el = this.view('tgt_metric');
                point = line.end;
                el.set('x', point.x);
                el.set('y', point.y + 10);
                el.set('text', this.targetmetric());
                el.set('transform', 'rotate(' + angle + ' ' + point.x + ',' + point.y + ')');
                el.setStyle('font-size', 12 * stageScale);
                el.setStyle('fill', '#689CD2');
            }
        }
     }
 });
 var topo = new nx.graphic.Topology({
     // width 100% if true
					'adaptive': true,
					// show icons' nodes, otherwise display dots
					'showIcon': true,
					// special configuration for nodes
					'nodeConfig': {
						'label': 'model.name',
						'iconType': 'router',
						'color': '#0how00'
					},
					// special configuration for links
					'linkConfig': {
						'linkType': 'curve',
						'color': "model.color",
						'sourcemetric': 'model.src_metric',
						'targetmetric': 'model.src_metric',
						'sourcelabel': 'model.src_network',
						'targetlabel': 'model.tgt_network'
					},
					// property name to identify unique nodes
					'identityKey': 'id', // helps to link source and target
					// canvas size
					'weight': 1800,
					'height': 900,
					// "engine" that process topology prior to rendering
					'dataProcessor': 'force',
					// moves the labels in order to avoid overlay
					'enableSmartLabel': true,
					// smooth scaling. may slow down, if true
					'enableGradualScaling': true,
					// if true, two nodes can have more than one link
					'supportMultipleLink': true,
					// enable scaling
					"scalable": true,
					linkInstanceClass: 'MyExtendLink'
        });
    topo.on('ready', function() {
        topo.data(topologyData);
     });

    var app = new nx.ui.Application();
    topo.attach(app);

})(nx);